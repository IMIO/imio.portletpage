# -*- coding: utf-8 -*-
from imio.portletpage.testing import (
    IMIO_PORTLETPAGE_FUNCTIONAL_TESTING,
    IMIO_PORTLETPAGE_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles, TEST_USER_ID
from plone.portlets.interfaces import IPortletType
from zope.component import getUtility

import unittest


class PortletIntegrationTest(unittest.TestCase):

    layer = IMIO_PORTLETPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_text_is_registered(self):
        portlet = getUtility(IPortletType, name="imio.portletpage.portlets.Text")
        self.assertEqual(portlet.addview, "imio.portletpage.portlets.Text")


class PortletFunctionalTest(unittest.TestCase):

    layer = IMIO_PORTLETPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
