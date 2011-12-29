from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class CollectiveLayer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.oembed
        self.loadZCML(package=collective.oembed)

        # Install product and call its initialize() function
        z2.installProduct(app, 'collective.oembed')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.oembed:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.oembed')

FIXTURE = CollectiveLayer()

INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="OEmbed:Integration")
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="OEmbed:Functional")
