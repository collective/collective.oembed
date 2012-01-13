from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

class PicasaWebURLEndPoint(base.UrlToOembed):
    """Picasaweb transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template="""<embed type="application/x-shockwave-flash" src="http://picasaweb.google.com/s/c/bin/slideshow.swf"
       pluginspage="http://www.macromedia.com/go/getflashplayer"
       width="%(width)s" height="%(height)s" flashvars="%(flashvars)s">
     </embed>"""

    url_schemes = ["http*://picasaweb.google.com*/*/*#*",
                   "http*://picasaweb.google.com*/lh/photo/*",
                   "http*://picasaweb.google.com*/*/*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
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

