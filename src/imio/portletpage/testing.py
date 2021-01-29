# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import imio.portletpage


class ImioPortletpageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.portletpage)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'imio.portletpage:default')


IMIO_PORTLETPAGE_FIXTURE = ImioPortletpageLayer()


IMIO_PORTLETPAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_PORTLETPAGE_FIXTURE,),
    name='ImioPortletpageLayer:IntegrationTesting',
)


IMIO_PORTLETPAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_PORTLETPAGE_FIXTURE,),
    name='ImioPortletpageLayer:FunctionalTesting',
)


IMIO_PORTLETPAGE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_PORTLETPAGE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ImioPortletpageLayer:AcceptanceTesting',
)
