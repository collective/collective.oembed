from urlparse import urlsplit
from urllib import quote, urlencode

import oembed

DEFAULT_SIZE = 400

class UrlToOembed(oembed.OEmbedEndpoint):
    """URLEndpoint is able to build embed html snippet just from the URL.
    It is not able to get Title and description data.
    
    Child classes must define their own embeding template, as well as the 
    request method to return the actual embeding code.
    """
    embed_html_template="""%(width)s%(height)s%(flashvar)s"""
    url_schemes = None

    def __init__(self):

        #Since classes derived from this one will deal with services
        #not supporting oEmbed, they won't need the provider's endpoint url
        super(UrlToOembed, self).__init__('', urlSchemes=self.url_schemes)
        
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

    def request(self, url):
        """Child classes must implement this method.
        
        Extract information from url needed by the template
        """
        raise NotImplementedError

    def get_embed(self, url, maxwidth=None, maxheight=None):
        """Build the embeding code from the given url according to the child
        class' template and return it
        """
        info = self.request(url)
        w, h = self.get_width_and_height(maxwidth=maxwidth,
                                         maxheight=maxheight)

        info['width'] = w
        info['height'] = h
        return self.embed_html_template%info
