import re
import urllib
import urllib2
import json
import logging

from zope import component
from zope import interface

import oembed
from plone.registry.interfaces import IRegistry

from collective.oembed import interfaces
from collective.oembed import endpoints
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    from collective.embedly.interfaces import IEmbedlySettings
    HAS_COLLECTIVE_EMBEDLY = True
except ImportError,e:
    HAS_COLLECTIVE_EMBEDLY = False

logger = logging.getLogger('collective.oembed')

TEMPLATES = {u"link":u"""
    <div class="oembed-wrapper oembed-link">
      <a href="%(url)s" target="_blank">%(title)s"></a>
      <div>%(html)s</div>
    </div> 
    """,
                 u"photo":u"""
    <div class="oembed-wrapper oembed-photo">
      <p><a href="%(url)s" target="_blank">%(title)s">
        <img src="%(url)s" alt="%(title)s"/>
      </a></p>
      <div>%(html)s</div>
    </div> 
    """,
                 u"rich":u"""
    <div class="oembed-wrapper oembed-rich">
      %(html)s
    </div> 
    """,
                 u"video":u"""
    <div class="oembed-wrapper oembed-video">
      %(html)s
    </div> 
    """}

class Consumer(object):
    """Consumer utility"""
    interface.implements(interfaces.IConsumer)

    def __init__(self):
        self.consumer = None
        self.embedly_apikey = None

    def get_data(self, url, maxwidth=None, maxheight=None,
                          format='json'):
        self.initialize_consumer()
        request = {}
        if maxwidth is not None:
            request['maxwidth'] = maxwidth
        if maxheight is not None:
            request['maxheight'] = maxheight
        request['format'] = format

        try:
            response = self.consumer.embed(url,**request)
            return response.getData()
        except oembed.OEmbedNoEndpoint, e:
            logger.info(e)
        except oembed.OEmbedError, e:
            #ofter a mimetype error
            logger.info(e)
        except urllib2.HTTPError, e:
            logger.info(e)

    def initialize_consumer(self):
        if self.consumer is None:

            consumer = oembed.OEmbedConsumer()
            _enpoints = endpoints.load_all_endpoints(embedly_apikey=self.embedly_apikey)
            for endpoint in _enpoints:
                consumer.addEndpoint(endpoint)

            self.consumer = consumer

    def get_embed(self, url, maxwidth=None, maxheight=None, format='json'):
        data = self.get_data(url, maxwidth=maxwidth, maxheight=maxheight,
                             format=format)
        if data is None or u"type" not in data:
            return u""
        return TEMPLATES[data[u"type"]]%data

class ConsumerView(BrowserView):
    """base browserview to display embed stuff"""

    embed_templates = {u'photo': ViewPageTemplateFile('oembed_photo.pt'),
                 u'video': ViewPageTemplateFile('oembed_video.pt'),
                 u'link':  ViewPageTemplateFile('oembed_link.pt'),
                 u'rich':  ViewPageTemplateFile('oembed_rich.pt')}

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.data = None
        self._utility = None
        self._url = None
        self._format = "json"
        self._maxwidth = None
        self._maxheight = None
        self.embeded = u""



    def update(self):
        """initialize all data"""
        if self._utility is None:
            self._utility = component.getUtility(interfaces.IConsumer)
            self._utility.embedly_apikey = self.get_embedly_apikey()

        if self._url is None:
            self._url = self.context.getRemoteUrl()

    def update_data(self):
        """load data extracted from the context"""
        self.update()
        if self.data is None:
            self.data = self._utility.get_data(self._url,
                                               maxwidth=self._maxwidth,
                                               maxheight=self._maxheight,
                                               format=self._format)

    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
        self.update()
        self.data = self._utility.get_data(url,
                                      maxwidth=maxwidth,
                                      maxheight=maxheight,
                                      format=format)
        return self.data

    def get_embed(self, url, maxwidth=None, maxheight=None, format='json'):

        data = self.get_data(url, maxwidth, maxheight, format)
        return self.display_data(data)

    def get_embed_auto(self):
        """This method extract params from the context"""
        self.update()
        self.update_data()
        return self.display_data(self.data)

    def display_data(self, data):
        if data is None:
            return u""

        if u'type' not in data:
            logger.info('no type in data for %s'%url)

        template = self.embed_templates.get(data[u'type'])

        return template(self)

    def get_embedly_apikey(self):
        """Return the api key from collective.embedly if found or from
        our own settings"""
        proxy = None
        registry = component.queryUtility(IRegistry)

        if registry is None:
            return

        if HAS_COLLECTIVE_EMBEDLY:
            try:
                proxy = registry.forInterface(IEmbedlySettings)
                return proxy.api_key
            except KeyError, e:
                pass

        try:
            proxy = registry.forInterface(interfaces.IOEmbedSettings)
            return proxy.embedly_apikey
        except KeyError, e:
            pass
