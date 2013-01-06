from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces


class GistGithubURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = """<script src="%(url)s.js"></script>"""
    oembed_type = "rich"
    url_schemes = ["https://gist.github.com/*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
#        proto, host, path, query_params, fragment = self.break_url(url)
#        splited = path.split('/')
#        len_ = len(splited)
        return {"url": url}
