from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces
from collective.oembed.url2embed.base import OembedHTMLParser

TEMPLATE = """<object type="application/x-shockwave-flash"
  data="http://360.io/static/flash/fbviewer.swf"
  width="%(width)s" height="%(height)s">
  <param name="movie" value="http://360.io/static/flash/fbviewer.swf"></param>
  <param name="quality" value="high"></param>
  <param name="allowFullScreen" value="true"></param>
  <param name="allowScriptAccess" value="always"></param>
  <param name="pluginspage"
  value="http://www.macromedia.com/go/getflashplayer"></param>
  <param name="autoplay" value="false"></param>
  <param name="autostart" value="false"></param>
  <param name="flashvars" value="%(flashvar)s"></param>
  <embed src="http://360.io/static/flash/fbviewer.swf"
  flashvars="%(flashvar)s"
  width="%(width)s" height="%(height)s"
  type="application/x-shockwave-flash"></embed></object>
"""

base_viewer = "http://360.io/static/flash/fbviewer.swf?"


class Occipital360HTMLParser(OembedHTMLParser):

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


class Occipital360EndPoint(base.UrlCrawlerToEmbed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = TEMPLATE
    oembed_type = "video"
    parser_klass = Occipital360HTMLParser

    url_schemes = ["http://360.io/*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        self.parse(url)
        return {'url': self.parser.video_url,
                'flashvar': self.parser.flashvar}
