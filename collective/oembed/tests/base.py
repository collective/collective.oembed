import unittest2 as unittest
from zope import interface
from plone.app import testing
from collective.oembed.tests import layer
from collective.oembed.tests import utils



class UnitTestCase(unittest.TestCase):
    
    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.oembed.interfaces import OEmbedLayer
        super(UnitTestCase, self).setUp()
        self.context = utils.FakeContext()
        self.request = utils.Request()
        interface.alsoProvides(self.request,
                               (IAttributeAnnotatable,OEmbedLayer))

class TestCase(unittest.TestCase):

    layer = layer.INTEGRATION

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.oembed.interfaces import OEmbedLayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable,OEmbedLayer))
        super(TestCase, self).setUp()
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.setTitle('Test folder')


class FunctionalTestCase(unittest.TestCase):

    layer = layer.FUNCTIONAL

    def setUp(self):
        from zope.annotation.interfaces import IAttributeAnnotatable
        from collective.oembed.interfaces import OEmbedLayer
        interface.alsoProvides(self.layer['request'],
                               (IAttributeAnnotatable,OEmbedLayer))
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.setTitle('Test folder')

def build_test_suite(test_classes):
    suite = unittest.TestSuite()
    for klass in test_classes:
        suite.addTest(unittest.makeSuite(klass))
    return suite
