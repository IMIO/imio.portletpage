# -*- coding: utf-8 -*-

from imio.portletpage.interfaces import IPortletTemplate
from zope.interface import implementer


@implementer(IPortletTemplate)
class PortletTemplateAdapter(object):
    """Base Portlet Template Adapter class"""
    # This must be overrided by sub classes
    template = None
    title = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return self.template()
