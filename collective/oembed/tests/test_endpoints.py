from collective.oembed.tests import base


class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import endpoints
        self.module = endpoints
        self.regex_providers = endpoints.REGEX_PROVIDERS

    def test_get_structure(self):
        from collective.oembed import endpoints
        structure = endpoints.get_structure()
        len_endpoints = len(structure)
        self.assertTrue(len_endpoints > 0)
        for hostname in structure:
            endpoints = structure[hostname]
            for endpoint in endpoints:
                self.assertIn(u'regex', endpoint)
                self.assertIn(u'factory', endpoint)
                self.assertIn(u'consumer', endpoint)
                self.assertIn(u'endpoint', endpoint)
                endpoint_instance = endpoint['factory'](endpoint)
                self.assertIsNotNone(endpoint_instance)
                consumer_instance = endpoint['consumer'](endpoint_instance)
                self.assertIsNotNone(consumer_instance)

    def test_WordpressEndPoint(self):
        from collective.oembed import endpoints
        wordpress = endpoints.WordpressEndPoint()
        url = 'http://public-api.wordpress.com/oembed/1.0/'
        self.assertEqual(wordpress._urlApi, url)
        request_url = 'http://toutpt.wordpress.com/2011/02/10/'
        request_url += 'collective-portlet-itemview/'
        request = wordpress.request(request_url)
        self.assertTrue(request.startswith(url))

    def test_EmbedlyEndPoint(self):
        from collective.oembed import endpoints
        embedly = endpoints.EmbedlyEndPoint('fakeapikey')
        url = 'http://api.embed.ly/1/oembed'
        self.assertEqual(embedly._urlApi, url)
        request_url = 'http://dontcare.com/toto'
        request = embedly.request(request_url)
        self.assertTrue(request.startswith(url))
        self.assertIn('key=fakeapikey', request)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test,))
