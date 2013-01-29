import urllib2

from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

CALENDAR_URL = 'https://www.google.com/calendar/embed?src=%(id)s'


class GoogleCalendarURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template = """<iframe src="%(url)s" style="border: 0"
       width="%(width)s" height="%(height)s" frameborder="0" scrolling="no">
      </iframe>"""
    oembed_type = "rich"

    url_schemes = ["https://www.google.com/calendar/feeds/*",
                   "https://www.google.com/calendar/ical/*",
                   "https://www.google.com/calendar/embed?*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        proto, host, path, query_params, fragment = self.break_url(url)
        splited = path.split('/')
        if (
            path.startswith('/calendar/feeds/') or
            path.startswith('/calendar/ical')
        ):
            if len(splited) > 2:
                cid = urllib2.unquote(splited[3])
        elif path.startswith('/calendar/embed'):
            cid = query_params.get('src', None)
            if id is not None:
                cid = urllib2.unquote(cid)

        gurl = CALENDAR_URL % {'id': cid}

        return {"url": gurl}
