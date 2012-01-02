from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import endpoints
        self.module = endpoints
        self.regex_providers = endpoints.REGEX_PROVIDERS
    
    def test_load_all_endpoints(self):
        from collective.oembed import endpoints
        all_endpoints = endpoints.load_all_endpoints()
        len_endpoints = len(all_endpoints)
        self.failUnless(len_endpoints>0)
        
        all_endpoints = endpoints.load_all_endpoints(embedly_apikey="fakeapikey")
        self.failUnless(len(all_endpoints)==len_endpoints + 1)

    def test_WordpressEndPoint(self):
        from collective.oembed import endpoints
        wordpress = endpoints.WordpressEndPoint()
        url = 'http://public-api.wordpress.com/oembed/1.0/'
        self.failUnless(wordpress._urlApi==url)
        request_url = 'http://toutpt.wordpress.com/2011/02/10/collective-portlet-itemview/'
        request = wordpress.request(request_url)
        self.failUnless(request.startswith(url))

    def test_EmbedlyEndPoint(self):
        from collective.oembed import endpoints
        embedly = endpoints.EmbedlyEndPoint('fakeapikey')
        url = 'http://api.embed.ly/1/oembed'
        self.failUnless(embedly._urlApi==url)
        request_url = 'http://dontcare.com/toto'
        request = embedly.request(request_url)
        self.failUnless(request.startswith(url))
        self.failUnless('key=fakeapikey' in request)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test,))
