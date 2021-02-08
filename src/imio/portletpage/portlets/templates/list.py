# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.portletpage import _
from imio.portletpage.portlets.adapters import PortletTemplateAdapter


class ListTemplate(PortletTemplateAdapter):
    template = ViewPageTemplateFile("list.pt")
    title = _("List")
