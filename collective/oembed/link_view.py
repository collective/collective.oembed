from urllib2 import urlopen, URLError
from urlparse import urlsplit

from zope import component
from plone.memoize.ram import cache

from Products.Five.browser import BrowserView

def _render_details_cachekey(method, self, url, maxwidth=None, maxheight=None,
                             format='json'):
    return '%s-%s-%s-%s'%(url, maxwidth, maxheight, format)


class LinkView(BrowserView):
    """Aggregate all services in the following order: 
      * oembed
      * api2embed
      * url2embed
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.oembed = None
        self.api2embed = None
        self.url2embed = None
    
    def update(self):
        if self.oembed is None:
            self.oembed = component.getMultiAdapter((self.context,self.request),
                                                name="oembed_view")
        if self.url2embed is None:
            self.url2embed = component.getMultiAdapter((self.context,
                                                        self.request),
                                                   name="url2embed_view")
    @cache(_render_details_cachekey)
    def get_embed(self, url, maxwidth=None, maxheight=None):
        return self.get_embed_uncached(url,
                                maxwidth=maxwidth,
                                maxheight=maxheight)

    def get_embed_uncached(self, url, maxwidth=None, maxheight=None):
        self.update()
        url = self.unshort_url(url)
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

    def get_embed_auto(self):
        url = self.context.getRemoteUrl()
        return self.get_embed(url)

    def unshort_url(self, url):
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