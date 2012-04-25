import urllib
import urllib2
import json
import logging
import oembed

from urllib2 import urlopen, URLError
from urlparse import urlsplit

from zope import component
from zope import interface

from plone.registry.interfaces import IRegistry
from plone.memoize.ram import cache

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

    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
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
            #often a mimetype error
            logger.info(e)
        except urllib2.HTTPError, e:
            logger.info(e)
        except URLError,e:
            #support offline mode
            logger.info('offline mode')

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
        if self._url is None:
            self._url = self.context.getRemoteUrl()
        self.update()
        self.update_data()
        return self.display_data(self.data)

    def display_data(self, data):
        if data is None:
            return u""

        if u'type' not in data:
            logger.info('no type in data for %s'%self._url)

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

def _render_details_cachekey(method, self, url, maxwidth=None, maxheight=None,
                             format='json'):
    return '%s-%s-%s-%s'%(url, maxwidth, maxheight, format)


class ConsumerAggregatedView(BrowserView):
    """This class is a super consumer. It use oembed and url2embed"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.oembed = None
        self.api2embed = None
        self.url2embed = None

    def update(self):
        if self.oembed is None:
            self.oembed = component.queryMultiAdapter((self.context,self.request),
                                                name="collective.oembed.consumer")

        if self.url2embed is None:
            self.url2embed = component.queryMultiAdapter((self.context,
                                                        self.request),
                                                   name="collective.oembed.url2embed")

#    @cache(_render_details_cachekey)
    def get_embed(self, url, maxwidth=None, maxheight=None):
        return self.get_embed_uncached(url,
                                maxwidth=maxwidth,
                                maxheight=maxheight)

    def get_embed_uncached(self, url, maxwidth=None, maxheight=None):

        self.update()
        url = unshort_url(url)
        embed = None

        if self.oembed is not None:
            embed = self.oembed.get_embed(url,
                                          maxwidth=maxwidth,
                                          maxheight=maxheight)

        if not embed and self.url2embed is not None:
            embed = self.url2embed.get_embed(url,
                                             maxwidth=maxwidth,
                                             maxheight=maxheight)

        return embed

def unshort_url(url):
    host = urlsplit(url)[1]

    if host in SHORT_URL_DOMAINS:
        try:
            response = urlopen(url, )
            return response.url
        except URLError:
            pass

    return url

SHORT_URL_DOMAINS = [
  'tinyurl.com',
  'goo.gl',
  'bit.ly',
  't.co',
  'youtu.be',
  'vbly.us',
]