# -*- coding: utf-8 -*-

from imio.portletpage.interfaces import IPortletTemplate
from imio.portletpage.portlets.adapters import PortletTemplateAdapter
from imio.smartweb.locales import SmartwebMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.component import named
from zope.interface import implementer
from zope.interface import Interface


@named("list")
@adapter(Interface, Interface, Interface)
@implementer(IPortletTemplate)
class ListTemplate(PortletTemplateAdapter):
    template = ViewPageTemplateFile("list.pt")
    title = _("List")
