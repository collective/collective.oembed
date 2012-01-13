from collective.oembed.url_to_oembed import base

class PicasaWebURLEndPoint(base.UrlToOembed):
    EMBED_HTML="""<embed type="application/x-shockwave-flash" src="http://picasaweb.google.com/s/c/bin/slideshow.swf"
       pluginspage="http://www.macromedia.com/go/getflashplayer"
       width="%(width)s" height="%(height)s" flashvars="%(flashvars)s">
     </embed>"""
     
    PICASA_URL_SCHEMES = ["http://picasaweb.google.com*/*/*#*",
                          "http://picasaweb.google.com*/lh/photo/*",
                          "http://picasaweb.google.com*/*/*"]
     
    def __init__(self):
        """A Picasa web dedicated class acting like a
        oEmbed endpoint.
        """
        super(PicasaWebURLEndPoint, self).__init__(self.PICASA_URL_SCHEMES)
        
    def request(self, url, **opts):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
    
        params = self.get_params_from_url(url)
        
        w, h = self.get_width_and_height(**opts)
        params["width"] = w
        params["height"] = h
        
        return self.EMBED_HTML % (params)
    
    def get_params_from_url(self, url):
        """Extracts only the relevant information from the url,
        and return it as a dict to be updated with additional params.
        """
        
        
        proto, host, path, query_params, fragment = self.break_url(url)
        # User ID and album name are in the path segment of the url
        userId = path.split("/")[-2]
        albumName = path.split("/")[-1]
        
        authKey = query_params.get("authkey", "")
        feat = query_params.get("feat", "")
        
        feedUrl = "http://picasaweb.google.com/data/feed/api/user/%s/album/%s?kind=photo&alt=rss&authkey=%s" % \
            (userId, albumName, authKey)
        
        flashVars = 'host=picasaweb.google.com&amp;feat=flashalbum&amp;RGB=0x000000&amp;' + \
            self._urlEncoder({'feed':feedUrl})
        
        return {"flashvars":flashVars}
        
        
    #def get(self, url):
        
        
