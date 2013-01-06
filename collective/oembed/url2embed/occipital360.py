import urllib2
from HTMLParser import HTMLParser, HTMLParseError

from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

TEMPLATE = """<object type="application/x-shockwave-flash"
 data="http://360.io/static/flash/fbviewer.swf" width="%(width)s"
 height="%(height)s">
 <param name="movie" value="http://360.io/static/flash/fbviewer.swf"></param>
 <param name="quality" value="high"></param>
 <param name="allowFullScreen" value="true"></param>
 <param name="allowScriptAccess" value="always"></param>
 <param name="pluginspage" value="http://www.macromedia.com/go/getflashplayer">
 </param>
 <param name="autoplay" value="false"></param>
 <param name="autostart" value="false"></param>
 <param name="flashvars" value="%(flashvar)s"></param>
 <embed src="http://360.io/static/flash/fbviewer.swf"
   flashvars="%(flashvar)s" width="%(width)s" height="%(height)s"
   type="application/x-shockwave-flash"></embed>
</object>
"""

base_viewer = "http://360.io/static/flash/fbviewer.swf?"


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []
        self.thumb = ""
        self.flashvar = ""
        self.description = ""
        self.title = ""
        self.width = ""
        self.height = ""

    def handle_starttag(self, tag, attrs):
        if tag == "link":
            if ("rel", "thumbnailUrl") in attrs:
                for attr, value in attrs:
                    if attr == "href":
                        self.thumb = value
        elif tag == "meta":
            if ("property", "og:image") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.images.append(value)
            elif ("property", "og:description") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.description = value
            elif ("property", "og:title") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.title = value
            elif ("property", "og:video:width") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.width = value
            elif ("property", "og:video:height") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.height = value
            elif ("property", "og:video") in attrs:
                for attr, value in attrs:
                    if attr == "content":
                        self.video_url = value
                        self.flashvar = self.video_url[len(base_viewer):]

    def has_finished(self):
        return bool(self.flashvar)

    def update_data(self, data):
        data[u'title'] = self.title
        data[u'width'] = self.width
        data[u'height'] = self.height


class Occipital360EndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = TEMPLATE
    oembed_type = "video"
    parser_klass = MyHTMLParser

    url_schemes = ["http://360.io/*"]

    def __init__(self):
        super(Occipital360EndPoint, self).__init__()
        self.parser = self.parser_klass()

    def parse(self, url):
        u = urllib2.urlopen(url).read()
        lines = u.split("\n")

        for line in lines:
            if self.parser.has_finished():
                break
            try:
                if not line.strip().startswith('<'):
                    continue
                self.parser.feed(line)
            except HTMLParseError, e:
                print e
                print line
                continue

    def get_embed(self, url, maxwidth=None, maxheight=None):
        #lets override this one
        info = self.request(url)
        info['width'] = self.parser.width
        info['height'] = self.parser.height
        return self.embed_html_template % info

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        super(Occipital360EndPoint, self).get_data(url,
                                                  maxwidth=maxwidth,
                                                  maxheight=maxheight,
                                                  format=format)
        self.parser.update_data(self.embed)
        return self.embed

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        self.parse(url)
        return {'flashvar': self.parser.flashvar}
