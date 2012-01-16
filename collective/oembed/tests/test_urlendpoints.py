from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import url2embed
        self.module = url2embed

    def test_picasaweb(self):
        endpoint = self.module.picasaweb.PicasaWebURLEndPoint()
        data = endpoint.get_embed('https://picasaweb.google.com/114389802187476114971/SE7EN?authkey=YkEcVtNL9g8&feat=featured#')
        self.failUnless(data is not None)

    def test_gistgithub(self):
        endpoint = self.module.gistgithub.GistGithubURLEndPoint()
        data = endpoint.get_embed('https://gist.github.com/1410787')
        self.failUnless(data is not None)

    def test_googlecalendar(self):
        endpoint = self.module.googlecalendar.GoogleCalendarURLEndPoint()

        data = endpoint.get_embed('https://www.google.com/calendar/feeds/fr.christian%23holiday%40group.v.calendar.google.com/public/basic')
        self.failUnless(data is not None)

        data = endpoint.get_embed('https://www.google.com/calendar/ical/fr.christian%23holiday%40group.v.calendar.google.com/public/basic.ics')
        self.failUnless(data is not None)

        data = endpoint.get_embed('https://www.google.com/calendar/embed?src=fr.christian%23holiday%40group.v.calendar.google.com&ctz=Europe/Paris')
        self.failUnless(data is not None)

    def test_googledocs(self):
        endpoint = self.module.googledocs.GoogleDocsURLEndPoint()

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

    def test_width_and_height(self):
        endpoint = self.module.base.UrlToOembed()

        w, h = endpoint.get_width_and_height()
        self.failUnless(w==h)
        self.failUnless(w==self.module.base.DEFAULT_SIZE)

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
