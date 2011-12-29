from collective.oembed.tests import base

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import consumer

    def testTitle(self):
        self.assertEqual("a","b")


class TestIntegration(base.TestCase):
    
    def testProperties(self):
        from collective.oembed import consumer
        self.failUnless(300 == 400)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
