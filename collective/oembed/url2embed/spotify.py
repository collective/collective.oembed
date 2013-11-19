from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces
from collective.oembed.url2embed.base import OembedHTMLParser

TEMPLATE = """<iframe src="https://embed.spotify.com/?uri=%(uri)s"
width="%(width)s" height="%(height)s" frameborder="0"
allowtransparency="true"></iframe>
"""


class HTMLParser(OembedHTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            if ("property", "og:image") in attrs:
                self._handleImage(attrs)
            elif ("property", "og:description") in attrs:
                self._handleDescription(attrs)
            elif ("property", "og:title") in attrs:
                self._handleTitle(attrs)
            elif ("property", "og:audio") in attrs:
                self._handleAudio(attrs)

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

    def _handleAudio(self, attrs):
        for attr, value in attrs:
            if attr == "content":
                self.audio = value

    def has_finished(self):
        return bool(self.flashvar)


class SpotifyEndPoint(base.UrlCrawlerToEmbed):
    """transform url to embed code"""

    interface.implements(interfaces.IURL2Embed)
    oembed_type = "rich"
    embed_html_template = TEMPLATE
    parser_klass = HTMLParser
    url_schemes = ["http://open.spotify.com/*"]
    default_height = 80
    default_width = 300

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        self.parse(url)
        return {"uri": url}
