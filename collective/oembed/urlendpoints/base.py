import oembed

class URLEndPoint(oembed.OEmbedEndpoint):
    """URLEndpoint is able to build embed html snippet just from the URL.
    It is not able to get Title and description data.
    """
    def __init__(self, urlSchemes=None):
        super(URLEndPoint, self).__init__('', urlSchemes=urlSchemes)

