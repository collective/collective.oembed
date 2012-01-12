import oembed

class URLResponse:
    """Fake OEmbedResponse object, containing the required
    json dictionnary.
    """
    
    def __init__(self, data):
        self._data = data
    
    def getData():
        return self._data
        
    def __getitem__(self, name):
        return self._data.get(name)

class URLEndPoint(oembed.OEmbedEndpoint):
    """URLEndpoint is able to build embed html snippet just from the URL.
    It is not able to get Title and description data.
    
    Child classes must define their own embeding template, as well as the 
    request method to return the actual embeding code.
    """
    EMBED_HTML="""%(width)s%(height)s%(flashvar)s"""
    
    def __init__(self, urlSchemes=None):
        """
        """
        #Since classes derived from this one will deal with services
        #not supporting oEmbed, they won't need the provider's endpoint url
        super(URLEndPoint, self).__init__('', urlSchemes=urlSchemes)
        
    def request(self, url, **opt):
        """Child classes must implement this method.
        
        Build the embeding code from the given url according to the child
        class' template. 
        
        Returns an URLResponse object behaving like a OEmbedResponse object.
        """
        raise NotImplementedError
        
    def get(self, url):
        """Return the embeding code.
        """
        return self.fetch(self.request(url, **opt))
        

