###
### Pour écraser la template 'edit-manager-contextual.pt'
###

# from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
# from plone.portlets.interfaces import IPortletManager
# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
# from zope.component import adapts
# from .content import IPortletPage

from plone.app.portlets.browser.editmanager import ContextualEditPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EditPortletManagerRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for contextual portlets"""

    #   adapts(IPortletPage, IDefaultBrowserLayer,
    #          IManageContextualPortletsView, IPortletManager)

    template = ViewPageTemplateFile("manager.pt")
