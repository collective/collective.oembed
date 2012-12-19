from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

TEMPLATE = """<iframe width="%(width)s" height="%(height)s"
frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
src="%(url)s"></iframe><br /><small>
<a href="%(original_url)s" style="color:#0000FF;text-align:left">
View it in a larger map</a>
</small>"""


class GoogleMapsURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = TEMPLATE
    oembed_type = "rich"

    url_schemes = ["http://maps.google.com*",
                   "https://maps.google.com*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """

        iframe_url = url + '&output=embed'
        return {"original_url": url,
                "url": iframe_url}
