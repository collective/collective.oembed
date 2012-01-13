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
