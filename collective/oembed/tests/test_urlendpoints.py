from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def test_picasaweb(self):
        from collective.oembed.url2embed import picasaweb
        endpoint = picasaweb.PicasaWebURLEndPoint()
        data = endpoint.get_embed('https://picasaweb.google.com/114389802187476114971/SE7EN?authkey=YkEcVtNL9g8&feat=featured#')
        self.failUnless(data is not None)

    def test_gistgithub(self):
        from collective.oembed.url2embed import gistgithub
        endpoint = gistgithub.GistGithubURLEndPoint()
        data = endpoint.get_embed('https://gist.github.com/1410787')
        self.failUnless(data is not None)

    def test_googlecalendar(self):
        from collective.oembed.url2embed import googlecalendar
        endpoint = googlecalendar.GoogleCalendarURLEndPoint()

        data = endpoint.get_embed('https://www.google.com/calendar/feeds/fr.christian%23holiday%40group.v.calendar.google.com/public/basic')
        self.failUnless(data is not None)

        data = endpoint.get_embed('https://www.google.com/calendar/ical/fr.christian%23holiday%40group.v.calendar.google.com/public/basic.ics')
        self.failUnless(data is not None)

        data = endpoint.get_embed('https://www.google.com/calendar/embed?src=fr.christian%23holiday%40group.v.calendar.google.com&ctz=Europe/Paris')
        self.failUnless(data is not None)

    def test_googledocs(self):
        from collective.oembed.url2embed import googledocs
        endpoint = googledocs.GoogleDocsURLEndPoint()

        #present
        url = 'https://docs.google.com/present/edit?id=0AcpVnMLn9OnaZGZxbWtqaG5fNDFtdmZtNWNo&hl=fr'
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

        #document
        url = 'https://docs.google.com/document/pub?id=1iuuTnIELWEVcJp1aUb_OXqXH2qHuT4AcGOiri7b10-g'
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

        #spreadheet
        url = 'https://docs.google.com/spreadsheet/pub?key=0AspVnMLn9OnadEFCQ2tMTHhkcHNkVDUyOWpZeE9ZMVE&output=html'
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

        #form
        url = 'https://docs.google.com/spreadsheet/viewform?formkey=dG9LWnM1ZWEtZEFORWNMaVBDVHQyeHc6MQ'
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

        #draw
        url = 'https://docs.google.com/drawings/pub?id=1nSnVgWPZdQJKQxIHkEofXqomf0n0xJSU9VhmxdjQsd8&w=960&h=720'
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

    def test_googlemaps(self):
        from collective.oembed.url2embed import googlemaps
        endpoint = googlemaps.GoogleMapsURLEndPoint()

        url = "http://maps.google.com/maps/ms?msid=212360783411321154030.00049a10cea932e12f6a3&msa=0"
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

    def test_scribd(self):
        from collective.oembed.url2embed import scribd
        endpoint = scribd.ScribdURLEndPoint()

        url = "http://www.scribd.com/fullscreen/78425441?access_key=key-112z96nfr7ixzj76rb3x"
        data = endpoint.get_embed(url)
        self.failUnless(data is not None)

    def test_width_and_height(self):
        from collective.oembed.url2embed import base as ubase
        endpoint = ubase.UrlToOembed()

        w, h = endpoint.get_width_and_height()
        self.failUnless(w==h)
        self.failUnless(w==ubase.DEFAULT_SIZE)

        w, h = endpoint.get_width_and_height(maxwidth=800)
        self.failUnless(w==h)
        self.failUnless(w==800)

        w, h = endpoint.get_width_and_height(maxheight=800)
        self.failUnless(w==h)
        self.failUnless(w==800)

        w, h = endpoint.get_width_and_height(maxwidth=800, maxheight=400)
        self.failUnless(w==800 and h==400)


class IntegrationTest(base.TestCase):

    def test_picasaweb(self):
        pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test,))
