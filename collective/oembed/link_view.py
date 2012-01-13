from zope import component

from Products.Five.browser import BrowserView

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
                                                name="link_oembed")
        if self.url2embed is None:
            self.url2embed = component.getMultiAdapter((self.context,
                                                        self.request),
                                                   name="url2embed_view")

    def get_embed(self, url, maxwidth=None, maxheight=None):
        self.update()
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
