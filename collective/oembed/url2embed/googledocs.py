import urllib2

from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

DOCUMENT_URL = 'https://docs.google.com/document/pub?id=%s&amp;embedded=true'
FORM_ULR = 'https://docs.google.com/spreadsheet/embeddedform?formkey=%s'
PRESENT_URL = "http://docs.google.com/present/embed?id=%s&ampelement=true"
SPREADSHEET_URL = "https://docs.google.com/spreadsheet/pub?key=%s&output=html"

IFRAME = """<iframe src="%(url)s" class="oembed-googledocs"
       width="%(width)s" height="%(height)s" frameborder="0" scrolling="no">
      </iframe>"""

PRESENT = """<iframe frameborder=0 marginwidth=0 marginheight=0 border=0
style="border:0;margin:0;width:%(width)spx;height:%(height)spx;"
src="%(url)s" scrolling="no" allowtransparency="true"></iframe>"""
DOCUMENT = """<iframe src="%(url)s" width="%(width)s" height="%(height)s"
frameborder="0" scrolling="no"></iframe>"""

IMG = """<img src="%(url)s&amp;w=%(width)s&amp;h=%(height)s">"""


class GoogleDocsURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)
    oembed_type = "rich"

    url_schemes = ["https://docs.google.com/drawings/pub?*",
                   "https://docs.google.com/spreadsheet/viewform?*",
                   "https://docs.google.com/present/edit?*",
                   "https://docs.google.com/document/pub?*",
                   "https://docs.google.com/spreadsheet/pub?*"]

    def __init__(self):
        super(GoogleDocsURLEndPoint, self).__init__()
        self._type = 'iframe'

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        proto, host, path, query_params = self.break_url(url)[0:4]
        gid = ''

        if path.startswith('/spreadsheet/viewform'):
            gid = query_params.get('formkey')
            gurl = FORM_ULR % urllib2.unquote(gid)
            self._type = 'form'
        elif path.startswith('/drawings/pub'):
            gid = query_params['id']
            gurl = '%s://%s%s?id=%s' % (proto, host, path, gid)
            self._type = 'img'
        elif path.startswith('/present/edit'):
            gid = query_params['id']
            gurl = PRESENT_URL % gid
            self._type = 'present'
        elif path.startswith('/document/pub'):
            gid = query_params['id']
            gurl = DOCUMENT_URL % gid
            self._type = 'document'
        elif path.startswith('/spreadsheet/pub'):
            gid = query_params['key']
            gurl = SPREADSHEET_URL % gid
            self._type = 'spreadsheet'

        return {'url': gurl}

    @property
    def embed_html_template(self):
        if self._type == 'iframe':
            return IFRAME
        elif self._type == 'form':
            return IFRAME
        elif self._type == 'present':
            return PRESENT
        elif self._type == 'document':
            return DOCUMENT
        elif self._type == 'spreadsheet':
            return IFRAME
        return IMG
