from urlparse import urlsplit
from urllib import quote, urlencode

import oembed

DEFAULT_SIZE = 400

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
        
        
class UrlToOembed(oembed.OEmbedEndpoint):
    """URLEndpoint is able to build embed html snippet just from the URL.
    It is not able to get Title and description data.
    
    Child classes must define their own embeding template, as well as the 
    request method to return the actual embeding code.
    """
    EMBED_HTML="""%(width)s%(height)s%(flashvar)s"""
    
    def __init__(self, urlSchemes=None):

        #Since classes derived from this one will deal with services
        #not supporting oEmbed, they won't need the provider's endpoint url
        super(UrlToOembed, self).__init__('', urlSchemes=urlSchemes)
        
        #Stores urllib.urlencode() in a member var to avoid reimporting it
        #in child classes
        self._urlEncoder = urlencode
        
    def break_url(self, url):
        """Beaks down the given url and returns each of its
        fragment to be processed by the caller
        """
    
        proto, host, path, query, fragment = urlsplit(url)
        path = quote(path)
        query = quote(query, safe='&=')
        fragment = quote(fragment, safe='')
        
        query_elems = {}
        # Put the query elems in a dict
        for pair in query.split('&'):
            pos = pair.find('=')
            if pos > -1:
                key = pair[:pos]
                value = pair[pos+1:]
            else:
                key = pair
                value = ''
            if key:
                query_elems[key] = value
                
        return proto, host, path, query_elems, fragment
        
    def get_width_and_height(self, maxwidth=None, maxheight=None):
        """Sets the width & height params to a default value if they werent 
        given.
        If only one param is given, then set the other one to same size.
        """
        
        if maxwidth is None:
            if maxheight is not None:
                maxwidth = maxheight
            else:
                maxwidth = DEFAULT_SIZE
                maxheight = DEFAULT_SIZE
        elif maxheight is None:
                maxheight = maxwidth
    
        return maxwidth, maxheight
        
      
    def request(self, url, **opt):
        """Child classes must implement this method.
        
        Build the embeding code from the given url according to the child
        class' template. 
        
        Returns an URLResponse object behaving like a OEmbedResponse object.
        """
        raise NotImplementedError
        
    def get_embed(self, url, **opts):
        """Return the embed code built by self.request
        """
        return self.request(url, **opts)
        

class UrlToOembedUtility(object):
    def __init__(self):
        self.endpoints = []