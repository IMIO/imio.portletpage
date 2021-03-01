# -*- coding: utf-8 -*-

from imio.portletpage.interfaces import IPortletTemplate
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, Interface, Interface)
@implementer(IPortletTemplate)
class PortletTemplateAdapter(object):
    """Base Portlet Template Adapter class"""

    # This must be overrided by sub classes
    template = None
    title = None

    def __init__(self, context, request, renderer):
        self.context = context
        self.request = request
        self.renderer = renderer

    def render(self):
        return self.template()

    @property
    def data(self):
        return self.context.data
