# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.portletpage.interfaces import IPortletTemplate
from imio.portletpage.portlets.adapters import PortletTemplateAdapter
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.component import adapter
from zope.component import named
from zope.interface import implementer
from zope.interface import Interface


@named("carousel")
@adapter(Interface, Interface, Interface)
@implementer(IPortletTemplate)
class CarouselTemplate(PortletTemplateAdapter):
    template = ViewPageTemplateFile("carousel.pt")
    title = _("Carousel")
