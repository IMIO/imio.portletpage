# -*- coding: utf-8 -*-
from plone import schema
from plone.app.portlets.interfaces import IPortletManager
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from imio.portletpage import _


class IPortletPageManager(IPortletManager):
    """Portlet page manager"""


class IPortletPage(model.Schema):
    """ Marker interface and Dexterity Python Schema for PortletPage
    """

    title = schema.TextLine(
        title=_(u"Title"),
        required=True
    )


@implementer(IPortletPage)
class PortletPage(Container):
    """
    """
