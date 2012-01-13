from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import url_to_oembed
        self.module = url_to_oembed
        
    
    def test_picasaweb(self):
        endpoint = self.module.picasaweb.PicasaWebURLEndPoint()
        data = endpoint.get('https://picasaweb.google.com/114389802187476114971/SE7EN?authkey=YkEcVtNL9g8&feat=featured#')
        self.failUnless(data is not None)
        


class IntegrationTest(base.TestCase):
    
    def test_picasaweb(self):
        pass


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test,))
