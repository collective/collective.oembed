from Products.Five.browser import BrowserView

from collective.oembed import interfaces

class API2EmbedView(BrowserView):
    """Aggregator of API2Embed view"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._utilities = []
        self._utility = None

    def update(self):
        if not self._utilities:
            self._utilities = component.getAllUtilitiesRegisteredFor(interfaces.IAPI2Embed)

    def get_embed(self, url, maxwidth=None, maxheight=None):
        self.update()
        endpoint = self.get_endpoint(url)
        if endpoint is not None:
            return endpoint.get_embed(url,
                                      maxwidth=maxwidth,
                                      maxheight=maxheight)

    def get_embed_auto(self):
        self.update()
        url = self.context.getRemoteUrl()
        endpoint = self.get_endpoint(url)
        if endpoint is not None:
            return endpoint.get_embed(url)

    def get_endpoint(self, url):
        if self._utility is None:
            for utility in self._utilities:
                if utility.match(url):
                    self._utility = utility

        return self._utility
