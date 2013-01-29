from collective.oembed.tests import base


class Test(base.UnitTestCase):

    def test_picasaweb(self):
        from collective.oembed.url2embed import picasaweb
        endpoint = picasaweb.PicasaWebURLEndPoint()
        url = 'https://picasaweb.google.com/114389802187476114971/SE7EN?'
        url += 'authkey=YkEcVtNL9g8&feat=featured#'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_gistgithub(self):
        from collective.oembed.url2embed import gistgithub
        endpoint = gistgithub.GistGithubURLEndPoint()
        data = endpoint.get_embed('https://gist.github.com/1410787')
        self.assertIsNotNone(data)

    def test_googlecalendar(self):
        from collective.oembed.url2embed import googlecalendar
        endpoint = googlecalendar.GoogleCalendarURLEndPoint()

        url = 'https://www.google.com/calendar/feeds/fr.christian%23holiday'
        url += '%40group.v.calendar.google.com/public/basic'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        url = 'https://www.google.com/calendar/ical/fr.christian%23holiday'
        url += '%40group.v.calendar.google.com/public/basic.ics'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        url = 'https://www.google.com/calendar/embed?src=fr.christian%23holida'
        url += 'y%40group.v.calendar.google.com&ctz=Europe/Paris'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_googledocs(self):
        from collective.oembed.url2embed import googledocs
        endpoint = googledocs.GoogleDocsURLEndPoint()

        #present
        url = 'https://docs.google.com/present/edit?id=0AcpVnMLn9OnaZGZxbWtqa'
        url += 'G5fNDFtdmZtNWNo&hl=fr'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        #document
        url = 'https://docs.google.com/document/pub?id=1iuuTnIELWEVcJp1aUb_OXq'
        url += 'XH2qHuT4AcGOiri7b10-g'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        #spreadheet
        url = 'https://docs.google.com/spreadsheet/pub?key=0AspVnMLn9OnadEFCQ2'
        url += 'tMTHhkcHNkVDUyOWpZeE9ZMVE&output=html'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        #form
        url = 'https://docs.google.com/spreadsheet/viewform?formkey=dG9LWnM1ZW'
        url += 'EtZEFORWNMaVBDVHQyeHc6MQ'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

        #draw
        url = 'https://docs.google.com/drawings/pub?id=1nSnVgWPZdQJKQxIHkEofXq'
        url += 'omf0n0xJSU9VhmxdjQsd8&w=960&h=720'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_googlemaps(self):
        from collective.oembed.url2embed import googlemaps
        endpoint = googlemaps.GoogleMapsURLEndPoint()

        url = 'http://maps.google.com/maps/ms?msid=212360783411321154030.0004'
        url += '9a10cea932e12f6a3&msa=0'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_scribd(self):
        from collective.oembed.url2embed import scribd
        endpoint = scribd.ScribdURLEndPoint()

        url = 'http://www.scribd.com/fullscreen/78425441?access_key=key-112z96'
        url += 'nfr7ixzj76rb3x'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_spotify(self):
        from collective.oembed.url2embed import spotify
        endpoint = spotify.SpotifyEndPoint()

        url = 'http://open.spotify.com/album/1VXa39MgJU8qDE1ASn9Wgp'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)
        self.assertTrue(data.startswith('<iframe'))

        data = endpoint.get_data(url)
        self.assertEqual(data['title'], u'WAR ON ERRORISM')

    def test_endpoint_itunes(self):
        from collective.oembed.url2embed import itunes
        endpoint = itunes.ITunesURLEndPoint()

        url = 'https://itunes.apple.com/fr/app/google-maps/id585027354'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)

    def test_occipital(self):
        from collective.oembed.url2embed import occipital360
        endpoint = occipital360.Occipital360EndPoint()

        url = 'http://360.io/jLnBUy'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)
        self.assertTrue(data.startswith('<object'))
        player = "http://360.io/static/flash/fbviewer.swf"
        self.assertIn(player, data)

    def test_issuu(self):
        from collective.oembed.url2embed import issuucom
        endpoint = issuucom.IssuuComEndPoint()

        url = 'http://issuu.com/humanizemagazine/docs/humanize19/1'
        data = endpoint.get_embed(url)
        self.assertIsNotNone(data)
        self.assertTrue(data.startswith('<object'))
        player = ("http://static.issuu.com/webembed/viewers/style1/v2/"
                  "IssuuReader.swf")
        self.assertIn(player, data)

    def test_width_and_height(self):
        from collective.oembed.url2embed import base as ubase
        endpoint = ubase.UrlToOembed()

        w, h = endpoint.get_width_and_height()
        self.assertEqual(w, h)
        self.assertEqual(w, ubase.DEFAULT_SIZE)

        w, h = endpoint.get_width_and_height(maxwidth=800)
        self.assertEqual(w, h)

        self.assertEqual(w, 800)

        w, h = endpoint.get_width_and_height(maxheight=800)
        self.assertEqual(w, h)

        self.assertEqual(w, 800)

        w, h = endpoint.get_width_and_height(maxwidth=800, maxheight=400)
        self.assertEqual(w, 800)
        self.assertEqual(h, 400)


class IntegrationTest(base.TestCase):

    def test_picasaweb(self):
        pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test,))
