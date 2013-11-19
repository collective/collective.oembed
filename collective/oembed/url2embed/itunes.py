from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

#https://itunes.apple.com/us/app/twitpic/id523490954
TEMPLATE = ('<iframe id="easyXDM_default1_provider" scrolling="no" '
            'width="%(width)s" height="%(height)s" '
            'frameborder="0" allowtransparency="false" tabindex="-1" '
            'role="presentation" name="easyXDM_default1_provider" '
            'src="https://itunes.apple.com/WebObjects/MZStore.woa/wa/'
            'viewSoftwareSocialPreview?cc=%(lang)s&amp;id=%(id)s&amp;'
            'mt=8&amp;wdId=32800">'
            '</iframe>')


class ITunesURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = TEMPLATE
    oembed_type = "rich"

    url_schemes = ["https://itunes.apple.com/*/app/*/id*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        proto, host, path, query_elems, fragment = self.break_url(url)

        splited = path.split('/')
        lang = splited[1]
#        appid = splited[3]
        id = splited[4][2:]
        return {"id": id,
                "lang": lang}
