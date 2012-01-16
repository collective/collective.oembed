import urllib2

from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

SCRIBD_URL = "http://www.scribd.com/embeds/%s/content?start_page=1&view_mode=list&access_key=%s"
#http://www.scribd.com/fullscreen/78425441?access_key=key-112z96nfr7ixzj76rb3x
#src="http://www.scribd.com/embeds/78425441/content?start_page=1&view_mode=list&access_key=key-112z96nfr7ixzj76rb3x" data-auto-height="true" data-aspect-ratio="0.608349900596421" scrolling="no" id="doc_82842" width="100%" height="600" frameborder="0"></iframe>

class ScribdURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template="""<iframe class="scribd_iframe_embed" src="%(url)s" data-auto-height="true" data-aspect-ratio="0.608349900596421" scrolling="no" id="doc_82842" width="%(width)s" height="%(height)s" frameborder="0"></iframe>
    <script type="text/javascript">(function() { var scribd = document.createElement("script"); scribd.type = "text/javascript"; scribd.async = true; scribd.src = "http://www.scribd.com/javascripts/embed_code/inject.js"; var s = document.getElementsByTagName("script")[0]; s.parentNode.insertBefore(scribd, s); })();</script>"""

    url_schemes = ["http://www.scribd.com/fullscreen/*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        proto, host, path, query_params, fragment = self.break_url(url)
        id = path.split('/')[-1]
        key = query_params['access_key']

        gurl = SCRIBD_URL%(id,key)

        return {"url":gurl}
