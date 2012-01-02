from collective.oembed.tests import base
from collective.oembed.tests import utils

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import viewlet
        self.viewlet = viewlet.JQueryOEmbedViewlet(self.context, 
                                                   self.request, None)
        self.viewlet.site_url = 'http://nohost' #no call to update()

    def test_display_condition(self):
        self.failUnless(self.viewlet.check_display_condition()==False)
        self.viewlet._settings = "aaa" #settings not None but not consistent
        self.failUnless(self.viewlet.check_display_condition()==False)
        self.viewlet._settings = utils.FakeProxy()
        self.viewlet._settings.activate_jqueryoembed_integration = True
        self.failUnless(self.viewlet.check_display_condition())

class TestIntegration(base.TestCase):

    def setUp(self):
        super(TestIntegration, self).setUp()
        from collective.oembed import viewlet
        self.viewlet = viewlet.JQueryOEmbedViewlet(self.portal, 
                                                   self.portal.REQUEST, None)
        self.viewlet.site_url = 'http://nohost' #no call to update()    

    def test_display_condition(self):
        self.failUnless(not self.viewlet.check_display_condition())
        self.viewlet.settings().activate_jqueryoembed_integration = True
        self.failUnless(self.viewlet.check_display_condition())

    def test_render(self):
        self.failUnless(not self.viewlet.render()) #should not display
        self.viewlet.settings().activate_jqueryoembed_integration = True
        text = self.viewlet.render()
        call_script = u'$(".oembed").oembed(null,jqueryOmebedSettings);' in text
        self.failUnless(call_script)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
