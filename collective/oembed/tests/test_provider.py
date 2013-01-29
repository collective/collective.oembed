from collective.oembed.tests import base
from collective.oembed.tests import utils


class Test(base.UnitTestCase):

    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import provider
        self.provider = provider.OEmbedProvider(self.context, self.request)

    def test_attributes(self):
        self.assertTrue(hasattr(self.provider, 'url'))
        self.assertTrue(hasattr(self.provider, 'maxwidth'))
        self.assertTrue(hasattr(self.provider, 'maxheight'))
        self.assertTrue(hasattr(self.provider, 'format'))

        self.assertIsNone(self.provider.url)
        self.assertIsNone(self.provider.maxwidth)
        self.assertIsNone(self.provider.maxheight)
        self.assertIsNone(self.provider.format)

    def test_update(self):
        self.request['url'] = 'http://nohost/test-folder'
        format_a = self.provider.format
        self.assertIsNone(format_a)

        self.provider.update()
        format_b = self.provider.format
        self.assertTrue(format_b == 'json')

        self.provider.format = None
        self.request['format'] = "xml"
        self.provider.update()
        format_c = self.provider.format
        self.assertEqual(format_c, 'xml')

        self.provider.format = None
        self.request['format'] = "wrong"
        self.assertRaises(ValueError, self.provider.update)

    def test_get_path(self):
        self.provider.url = 'http://nohost/test-folder'
        path = self.provider.get_path()
        self.assertEqual(path, '/test-folder')

        url = 'http://www.youtube.com/playlist?list=PL84E044CCF097C8CB'
        self.provider.url = url
        path = self.provider.get_path()
        self.assertEqual(path, '/playlist')

    def test_build_info(self):
        context = self.context
        site = utils.FakeContext()
        site.title = "My Plone site"
        site.id = "Plone"
        self.provider.build_info(context, site)
        data = self.provider.embed
        self.assertIsNotNone(data)
        self.assertEqual(data[u"type"], "rich")


class TestIntegration(base.TestCase):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.portal.REQUEST['url'] = self.folder.absolute_url()
        self.view = self.portal.restrictedTraverse('@@oembed')

    def test_call(self):
        render = self.view()
        self.assertTrue(render is not None)
        import json
        data = json.loads(render)
        self.assertIn(u'type', data)
        self.assertEqual(data[u'type'], u'link')
        self.assertEqual(data[u'title'], u'Test folder')

    def test_call_xml(self):
        self.portal.REQUEST['format'] = 'xml'
        render = self.view()
        self.assertIsNotNone(render is not None)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
