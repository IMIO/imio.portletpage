from zope.interface import implementer_only
from plone.app.portlets.browser.manage import ManageContextualPortlets
from plone.app.portlets.interfaces import ITopbarManagePortlets
from zope.component import getMultiAdapter

from plone.dexterity.browser import edit

## TODO vérifier l'utiliter de l'interface implementer_only

# @implementer_only(ITopbarManagePortlets)
class EditView(ManageContextualPortlets):
    def __init__(self, context, request):
        # Past the main parent constructor, since it sets disable_border
        super(ManageContextualPortlets, self).__init__(context, request)
        # Disable the left and right columns
        self.request.set("disable_plone.leftcolumn", 1)
        self.request.set("disable_plone.rightcolumn", 1)
