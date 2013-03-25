import re
import logging

from urllib2 import urlopen, URLError
from urlparse import urlsplit

from plone.memoize.ram import cache

from collective.oembed import endpoints
from collective.oembed.api2embed import structure as api2embed_structure
from collective.oembed.url2embed import structure as url2embed_structure
from Products.Five.browser import BrowserView
import time

#try:
#    from collective.embedly.interfaces import IEmbedlySettings
#    HAS_COLLECTIVE_EMBEDLY = True
#except ImportError, e:
#    HAS_COLLECTIVE_EMBEDLY = False

logger = logging.getLogger('collective.oembed')


def _render_details_cachekey(method, self, url, maxwidth=None, maxheight=None,
                             format='json'):
    one_hour = time.time() // (60 * 60)
    return '%s-%s-%s-%s-%s' % (url, maxwidth, maxheight, format, one_hour)


class ConsumerView(BrowserView):
    """This class is a super consumer. It use oembed and url2embed"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.structure = {}  # hostname / endpoint info
        self.checkers = []  # return endpoint if url match
        self._maxwidth = None
        self._maxheight = None

    def update(self):
        if not self.structure:
            s_endpoints = endpoints.get_structure()
            s_url2embed = url2embed_structure.get_structure()
            s_api2embed = api2embed_structure.get_structure()
            for providers in (s_endpoints, s_url2embed, s_api2embed):
                for hostname in providers:
                    if hostname not in self.structure:
                        self.structure[hostname] = []
                    infos = providers[hostname]
                    for info in infos:
                        self.structure[hostname].append(info)

        # TODO add plugable components for structure stuff
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

    def load_checkers(self):
        if not self.checkers:
            self.checkers += endpoints.get_checkers()
#            self.checkers.append(url2embed.get_checkers())
#            self.checkers.append(api2embed.get_checkers())

    @cache(_render_details_cachekey)
    def get_embed(self, url, maxwidth=None, maxheight=None):
        return self.get_embed_uncached(
            url,
            maxwidth=maxwidth,
            maxheight=maxheight
        )

    def get_embed_uncached(self, url, maxwidth=None, maxheight=None):
        #logger.info('request not in cache: get_embed(%s)' % url)
        url = unshort_url(url)
        self.url = url
        self.update()
        embed = None
        consumer = self.get_consumer(url)

        if consumer and not embed:
            embed = consumer.get_embed(
                url,
                maxwidth=maxwidth,
                maxheight=maxheight
            )

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
                #logger.info('find endpoint !')
                consumer = endpoint_info['consumer'](endpoint)
                return consumer
        logger.info('no endpoint match for %s. tried %s' % (url, endpoints))

    def get_endpoints(self, hostname="", url=""):
        """Return components responsible to handle this hostname"""

        if url:
            hostname = self.get_hostname(url)

        # First: Try to get it from key / value structure
        endpoints = list(self.structure.get(hostname, []))

        if endpoints:
            return endpoints

        if not self.checkers:
            self.load_checkers()

        for checker in self.checkers:
            if re.match(checker['regex'], url):
                return [checker]

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
