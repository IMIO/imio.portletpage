# -*- coding: utf-8 -*-
from imio.portletpage.content.portlet_page import IPortletPage  # NOQA E501
from imio.portletpage.testing import IMIO_PORTLETPAGE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class PortletPageIntegrationTest(unittest.TestCase):

    layer = IMIO_PORTLETPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_portlet_page_schema(self):
        fti = queryUtility(IDexterityFTI, name='PortletPage')
        schema = fti.lookupSchema()
        self.assertEqual(IPortletPage, schema)

    def test_ct_portlet_page_fti(self):
        fti = queryUtility(IDexterityFTI, name='PortletPage')
        self.assertTrue(fti)

    def test_ct_portlet_page_factory(self):
        fti = queryUtility(IDexterityFTI, name='PortletPage')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPortletPage.providedBy(obj),
            u'IPortletPage not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_portlet_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='PortletPage',
            id='portlet_page',
        )

        self.assertTrue(
            IPortletPage.providedBy(obj),
            u'IPortletPage not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('portlet_page', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('portlet_page', parent.objectIds())

    def test_ct_portlet_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PortletPage')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_portlet_page_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='PortletPage')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'portlet_page_id',
            title='PortletPage container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
