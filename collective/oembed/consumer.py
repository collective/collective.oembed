import re
import urllib
import urllib2
import json
import logging

from zope import component
from zope import interface
from plone.memoize.ram import cache

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

def _render_details_cachekey(method, self, url, maxwidth, maxheight, format):
    return '%s-%s-%s-%s'%(url, maxwidth, maxheight, format)


class Consumer(object):
    """Consumer utility"""
    interface.implements(interfaces.IConsumer)

    def __init__(self):
        self.consumer = None
        self.embedly_apikey = None
        self.site_domain = None

#    @cache(_render_details_cachekey)
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

    def initialize_consumer(self):
        consumer = oembed.OEmbedConsumer()
        if self.embedly_apikey is not None:
            endpoint = endpoints.EmbedlyEndPoint(self.embedly_apikey)
            consumer.addEndpoint(endpoint)

        endpoint = endpoints.WordpressEndPoint()
        consumer.addEndpoint(endpoint)

        providers = endpoints.REGEX_PROVIDERS
    
        for provider in providers:
            endpoint = oembed.OEmbedEndpoint(provider[u'endpoint'], provider[u'regex'])
            consumer.addEndpoint(endpoint)

        self.consumer = consumer


class ConsumerView(BrowserView):
    """base browserview to display embed stuff"""

    embed_templates = {u'photo': ViewPageTemplateFile('oembed_photo.pt'),
                 u'video': ViewPageTemplateFile('oembed_video.pt'),
                 u'link':  ViewPageTemplateFile('oembed_link.pt'),
                 u'rich':  ViewPageTemplateFile('oembed_rich.pt')}

    maxwidth = None
    maxheight = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._utility = None
        self.data = {}

    def url(self):
        return self.context.getRemoteUrl()

    def embed(self):
        consumer = self.consumer()
        consumer.embedly_apikey = self.embedly_apikey()
        url = self.url()
        self.data = consumer.get_data(url,
                                 maxwidth=self.maxwidth,
                                 maxheight=self.maxheight)

        if self.data is None:
            logger.info('no data for %s'%url)
            return u''

        if u'type' not in self.data:
            logger.info('no type in data for %s'%url)

        template = self.embed_templates.get(self.data[u'type'])

        return template(self)

    def consumer(self):
        if self._utility is None:
            self._utility = component.getUtility(interfaces.IConsumer)
        return self._utility

    def embedly_apikey(self):
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
            proxy = registry.forInterface(interfaces.IConsumerSettings)
            return proxy.embedly_apikey
        except KeyError, e:
            pass
