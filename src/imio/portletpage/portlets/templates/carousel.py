# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.portletpage import _
from imio.portletpage.portlets.adapters import PortletTemplateAdapter


class CarouselTemplate(PortletTemplateAdapter):
    template = ViewPageTemplateFile("carousel.pt")
    title = _("Carousel")
