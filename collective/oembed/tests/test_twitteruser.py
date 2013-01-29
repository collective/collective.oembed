from collective.oembed.tests import base
URL = "https://twitter.com/toutpt"


class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed.api2embed import twitteruser
        self.endpoint = twitteruser.TwitterUserAPI2Embed()

    def test_match(self):
        self.assertTrue(self.endpoint.match(URL))
        url = "https://twitter.com/toutpt/statuses/153185403766185985"
        self.assertFalse(self.endpoint.match(url))

    def test_get_embed(self):
        embed = self.endpoint.get_embed(URL)
        self.assertTrue(embed.startswith('<blockquote'))

    def test_get_data(self):
        data = self.endpoint.get_data(URL)
        for key in [u'provider_url', u'title', u'html', u'author_name',
                    u'version', u'author_url', u'provider_name', u'type']:
            self.assertIn(key, data)
        self.assertEqual(data['type'], 'rich')
        self.assertEqual(data['author_url'], 'https://twitter.com/toutpt')


class IntegrationTestCase(base.TestCase):

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal.REQUEST['url'] = URL
        self.view = self.portal.restrictedTraverse('@@proxy-oembed-provider')
        self.view.update()

    def test_get_embed(self):
        embed = self.view.get_embed(url=URL)
        self.assertTrue(embed.startswith('<blockquote'))

    def test_get_data(self):
        data = self.view.get_data(url=URL)
        for key in [u'provider_url', u'title', u'html', u'author_name',
                    u'version', u'author_url', u'provider_name', u'type']:
            self.assertIn(key, data)
        self.assertEqual(data['type'], 'rich')
        self.assertEqual(data['author_url'], 'https://twitter.com/toutpt')
