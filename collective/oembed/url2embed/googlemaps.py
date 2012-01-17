from zope import interface

from collective.oembed.url2embed import base
from collective.oembed import interfaces

MAPS_URL = 'http://maps.google.com/maps/ms?msa=%s&amp;msid=%s&amp;output=embed'

class GoogleMapsURLEndPoint(base.UrlToOembed):
    """transform url to embed code"""
    interface.implements(interfaces.IURL2Embed)

    embed_html_template="""<iframe width="%(width)s" height="%(height)s" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
    src="%(url)s"></iframe><br /><small><a href="http://maps.google.com/maps/ms?msa=0&amp;msid=212360783411321154030.00049a10cea932e12f6a3&amp;hl=en&amp;ie=UTF8&amp;t=v&amp;vpsrc=1&amp;ll=49.12945,8.721379&amp;spn=3.441779,8.739338&amp;source=embed" style="color:#0000FF;text-align:left">View it in a larger map</a></small>"""

    url_schemes = ["http://maps.google.com/maps/ms?*"]

    def request(self, url):
        """Extract the needed parameters from the given url and options,
        and return the embed code.
        """
        query_params = self.break_url(url)[3]

        msid = query_params['msid']
        msa = query_params['msa']

        gurl = MAPS_URL%(msa, msid)

        return {"url":gurl}
