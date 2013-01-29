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

    def update(self):
        if self.oembed is None:
            self.oembed = component.queryMultiAdapter(
                (self.context, self.request), name="proxy-oembed-provider"
            )

    def get_embed(self, url, maxwidth=None, maxheight=None):
        self.update()
        if self.oembed is not None:
            return self.oembed.get_embed(url,
                                         maxwidth=maxwidth,
                                         maxheight=maxheight)

    def get_embed_auto(self):
        url = self.context.getRemoteUrl()
        return self.get_embed(url)
