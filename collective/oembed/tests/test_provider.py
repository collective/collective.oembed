from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import provider
        self.provider = provider.OEmbedProvider(self.context, self.request)

    def test_attributes(self):
        self.failUnless(hasattr(self.provider,'url'))
        self.failUnless(hasattr(self.provider,'maxwidth'))
        self.failUnless(hasattr(self.provider,'maxheight'))
        self.failUnless(hasattr(self.provider,'format'))

        self.failUnless(self.provider.url is None)
        self.failUnless(self.provider.maxwidth is None)
        self.failUnless(self.provider.maxheight is None)
        self.failUnless(self.provider.format is None)

    def test_update(self):
        self.request['url'] = 'http://nohost/test-folder'
        format_a = self.provider.format
        self.failUnless(format_a is None)

        self.provider.update()
        format_b = self.provider.format
        self.failUnless(format_b == 'json')

        self.provider.format = None
        self.request['format']="xml"
        self.provider.update()
        format_c = self.provider.format
        self.failUnless(format_c == 'xml')

        self.provider.format = None
        self.request['format']="wrong"
        self.assertRaises(ValueError, self.provider.update)


    def test_get_path(self):
        self.provider.url = 'http://nohost/test-folder'
        path = self.provider.get_path()
        self.failUnless(path == '/test-folder')

        self.provider.url = 'http://www.youtube.com/playlist?list=PL84E044CCF097C8CB'
        path = self.provider.get_path()
        self.failUnless(path == '/playlist')

    def test_build_info(self):
        context = self.context
        site = utils.FakeContext()
        site.title = "My Plone site"
        site.id="Plone"
        self.provider.build_info(context, site)
        data = self.provider.embed
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]==u"link")

class TestIntegration(base.TestCase):
    
    def setUp(self):
        super(TestIntegration, self).setUp()
        self.view = self.portal.restrictedTraverse('@@oembed')
        self.portal.REQUEST['url']=self.folder.absolute_url()
    
    def test_call(self):
        render = self.view()
        self.failUnless(render is not None)
        import json
        data = json.loads(render)
        self.failUnless(u'type' in data)
        self.failUnless(data[u'type'] == u'link')
        self.failUnless(data[u'title'] == u'Test folder')
    
    def test_call_xml(self):
        self.portal.REQUEST['format']='xml'
        render = self.view()
        self.failUnless(render is not None)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
