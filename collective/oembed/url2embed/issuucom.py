from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces
from collective.oembed.url2embed.base import OembedHTMLParser

TEMPLATE = """<object type="application/x-shockwave-flash"
 data="http://static.issuu.com/webembed/viewers/style1/v2/IssuuReader.swf"
 width="%(width)s" height="%(height)s">
 <param
   name="movie"
   value="http://static.issuu.com/webembed/viewers/style1/v2/IssuuReader.swf">
 </param>
 <param name="quality" value="high"></param>
 <param name="allowFullScreen" value="true"></param>
 <param name="allowScriptAccess" value="always"></param>
 <param name="pluginspage" value="http://www.macromedia.com/go/getflashplayer">
 </param>
 <param name="autoplay" value="false"></param>
 <param name="autostart" value="false"></param>
 <param name="flashvars" value="%(flashvar)s"></param>
 <embed
   src="http://static.issuu.com/webembed/viewers/style1/v2/IssuuReader.swf"
   flashvars="%(flashvar)s" width="%(width)s" height="%(height)s"
   type="application/x-shockwave-flash"></embed>
</object>
"""

base_viewer = \
    "http://static.issuu.com/webembed/viewers/style1/v2/IssuuReader.swf?"


class HTMLParser(OembedHTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            if ("property", "og:image") in attrs:
                self._handleImage(attrs)
            elif ("property", "og:description") in attrs:
                self._handleDescription(attrs)
            elif ("property", "og:title") in attrs:
                self._handleTitle(attrs)
            elif ("property", "og:video:width") in attrs:
                self._handleVideoWidth(attrs)
            elif ("property", "og:video:height") in attrs:
                self._handleVideoHeight(attrs)
            elif ("property", "og:video") in attrs:
                self._handleVideo(attrs)

    def _handleImage(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.images.append(value)

    def _handleDescription(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.description = value

    def _handleTitle(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.title = value

    def _handleVideoWidth(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.width = value

    def _handleVideoHeight(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.height = value

    def _handleVideo(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.video_url = value
                self.flashvar = self.video_url[len(base_viewer):]

    def has_finished(self):
        return bool(self.width)


class IssuuComEndPoint(base.UrlCrawlerToEmbed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = TEMPLATE
    oembed_type = "video"
    parser_klass = HTMLParser

    url_schemes = ["http://issuu.com/*/docs/*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        self.parse(url)
        return {'flashvar': self.parser.flashvar}
