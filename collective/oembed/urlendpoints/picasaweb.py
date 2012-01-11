from collective.oembed.urlendpoints import base

class PicasaWebURLEndPoint(base.URLEndPoint):
    EMBED_HTML="""<embed type="application/x-shockwave-flash" src="http://picasaweb.google.com/s/c/bin/slideshow.swf"
       pluginspage="http://www.macromedia.com/go/getflashplayer"
       width="%(width)s" height="%(height)s" flashvars="%(flashvars)s">
     </embed>"""
