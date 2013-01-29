import urllib2
import logging
import oembed

from urllib2 import urlopen, URLError
from urlparse import urlsplit

from zope import component
from zope import interface

from plone.registry.interfaces import IRegistry
from plone.memoize.ram import cache

from collective.oembed import interfaces, url2embed, api2embed, endpoints
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import time

try:
    from collective.embedly.interfaces import IEmbedlySettings
    HAS_COLLECTIVE_EMBEDLY = True
except ImportError, e:
    HAS_COLLECTIVE_EMBEDLY = False

logger = logging.getLogger('collective.oembed')


class ConsumerView(BrowserView):
    """base browserview to display embed stuff"""

    embed_templates = {
        u'photo': ViewPageTemplateFile('oembed_photo.pt'),
        u'video': ViewPageTemplateFile('oembed_video.pt'),
        u'link':  ViewPageTemplateFile('oembed_link.pt'),
        u'rich':  ViewPageTemplateFile('oembed_rich.pt')
    }

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
            logger.info('no type in data for %s' % self._url)

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
    one_hour = time.time() // (60 * 60)
    return '%s-%s-%s-%s-%s' % (url, maxwidth, maxheight, format, one_hour)


class ConsumerAggregatedView(BrowserView):
    """This class is a super consumer. It use oembed and url2embed"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.structure = {}
#        self.oembed = None
#        self.api2embed = None
#        self.url2embed = None
        self._maxwidth = None
        self._maxheight = None

    def update(self):
        s_endpoints = endpoints.get_structure()
        s_url2embed = url2embed.get_structure()
        s_api2embed = api2embed.get_structure()
        for providers in (s_endpoints, s_url2embed, s_api2embed):
            for hostname in providers:
                if hostname not in self.structure:
                    self.structure[hostname] = []
                infos = providers[hostname]
                for info in infos:
                    self.structure[hostname].append(info)
#        registry = component.getUtility(IRegistry)
#        black_list = registry.get('collective.oembed.blacklist')
#        plugins = registry.get('collective.oembed.consumers')
#        for plugin in plugins:
#            try:
#                hostname, consumername = plugin.split('/')
#            except ValueError:
#                logger.error('can t extract consumer form %s' % plugin)
#                continue
#            self.structure[hostname] = consumer

    @cache(_render_details_cachekey)
    def get_embed(self, url, maxwidth=None, maxheight=None):
        return self.get_embed_uncached(url,
                                maxwidth=maxwidth,
                                maxheight=maxheight)

    def get_embed_uncached(self, url, maxwidth=None, maxheight=None):
        logger.info('request not in cache: get_embed(%s)' % url)
        self.update()
        url = unshort_url(url)
        embed = None
        providers = self.get_providers(url)

        for provider in providers:
            if provider and not embed:
                embed = provider.get_embed(url,
                                           maxwidth=maxwidth,
                                           maxheight=maxheight)

        return embed

    def get_embed_auto(self):
        """This method extract params from the context"""
        if self._url is None:
            self._url = self.context.getRemoteUrl()
        return self.get_embed(self._url,
                              self._maxwidth,
                              self._maxheight)

    @cache(_render_details_cachekey)
    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
        logger.info('request not in cache: get_data(%s)' % url)
        self.update()
        url = unshort_url(url)
        consumer = self.get_consumer(url)

        if consumer:
            data = consumer.get_data(
                url,
                maxwidth=maxwidth,
                maxheight=maxheight,
                format=format
            )

            return data

    def get_consumer(self, url):
        endpoints = self.get_endpoints(url=url)
        if not endpoints:
            return
        for endpoint_info in endpoints:
            if not endpoint_info:
                continue
            endpoint = endpoint_info['factory'](endpoint_info)
            if endpoint.match(url):
                logger.info('find endpoint !')
                consumer = endpoint_info['consumer'](endpoint)
                return consumer
        logger.info('no endpoint match for %s. tried %s' % (url, endpoints))

    def get_endpoints(self, hostname="", url=""):
        """Return components responsible to handle this hostname"""

        endpoints = []
        if url:
            hostname = self.get_hostname(url)
        endpoint = self.structure.get(hostname)

        if type(endpoint) in (list, tuple):
            for info in endpoint:
                endpoints.append(info)
        else:
            endpoints.append(endpoint)

        return endpoints

    def get_hostname(self, url):
        return urlsplit(url)[1]


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
