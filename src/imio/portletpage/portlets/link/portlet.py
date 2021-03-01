# -*- coding: utf-8 -*-
from imio.portletpage.interfaces import IPortletTemplate
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import schema
from plone.app.portlets.portlets import base
from plone.formwidget.namedfile.converter import NamedDataConverter
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import NamedFileWidget
from plone.memoize.instance import memoize
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.interfaces import INamedBlobFileField
from plone.portlets.interfaces import IPortletDataProvider
from plone.supermodel import model
from zope.schema.interfaces import IObject
from z3c.form.datamanager import AttributeField
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IObjectFactory
from z3c.form.interfaces import NOT_CHANGED
from z3c.form.interfaces import NO_VALUE
from z3c.form.object import FactoryAdapter
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import implementer_only
from zope.schema.fieldproperty import FieldProperty


class IIconBlobFile(INamedBlobFileField):
    pass


@implementer(IIconBlobFile)
class IconBlobFile(NamedBlobFile):
    pass


class IIconBlobFileWidget(INamedFileWidget):
    pass


@implementer_only(IIconBlobFileWidget)
class IconBlobFileWidget(NamedFileWidget):

    def extract(self, default=NO_VALUE):
        try:
            value = super(IconBlobFileWidget, self).extract(default=default)
        except UnboundLocalError:
            # This can happen on subform context
            value = default
        if value == default:
            return self._get_value()
        return value

    def _get_value(self, default=NO_VALUE):
        context = self.form.parentForm.context
        # We need the field name on the parent form and the sequence index that
        # we can extract from subform parent name : e.g. form.widgets.fieldname.0
        fieldname, idx = self.form._parent.name.split(".")[-2:]
        if hasattr(context, fieldname):
            idx = int(idx)
            values = getattr(context, fieldname)
            if idx >= len(values):
                # We are in the case where we add a new row
                return default
            row = values[idx]
            return getattr(row, self.field.__name__, default)
        return default


@implementer(IFieldWidget)
@adapter(IIconBlobFile, IFormLayer)
def IconBlobFileFieldWidget(field, request):
    return FieldWidget(field, IconBlobFileWidget(request))


@adapter(IIconBlobFile, IIconBlobFileWidget)
class IconDataConverter(NamedDataConverter):
    def toFieldValue(self, value):
        value = super(IconDataConverter, self).toFieldValue(value)
        if value == NOT_CHANGED:
            value = self.widget._get_value()
        return value


class ILinkRow(model.Schema):
    title = schema.TextLine(
        title=_(u"Title"),
        required=True
    )

    internal_url = schema.URI(
        title=_(u"Internal URL"),
        required=False,
    )

    external_url = schema.URI(
        title=_(u"External URL"),
        required=False,
    )

    icon = IconBlobFile(
        title=_(u"Icon"),
        required=True,
    )


@adapter(ILinkRow, IObject)
@implementer(IDataManager)
class LinkDataManager(AttributeField):
    pass


@implementer(ILinkRow)
class LinkRow(object):
    title = FieldProperty(ILinkRow["title"])
    internal_url = FieldProperty(ILinkRow["internal_url"])
    external_url = FieldProperty(ILinkRow["external_url"])
    icon = FieldProperty(ILinkRow["icon"])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''

    def __repr__(self):
        return "<LinkRow>"


@implementer(IObjectFactory)
@adapter(Interface, Interface, Interface, Interface)
class LinkRowAdapter(FactoryAdapter):
    factory = LinkRow


class ILinkPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Title"),
        required=True
    )

    template = schema.Choice(
        title=_(u"Template"),
        required=False,
        default=u"",
        vocabulary="imio.portletpage.PortletTemplates",
    )

    css_classes = schema.TextLine(
        title=_(u"CSS Classes"),
        description=_(u"CSS Classes to personnalize the portlet style"),
        required=False,
    )

    links = schema.List(
        title=_(u"Links"),
        description=_(u"List of links"),
        required=False,
        value_type=schema.Object(title=_(u"Link"), schema=ILinkRow),
    )


@implementer(ILinkPortlet)
class Assignment(base.Assignment):

    def __init__(self, header=u"", template=None, css_classes=u"", links=None):
        self.header = header
        self.template = template
        self.css_classes = css_classes
        self.links = links

    @property
    def title(self):
        return self.header


class AddForm(base.AddForm):
    schema = ILinkPortlet
    label = _(u'Add Link Portlet')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = ILinkPortlet
    label = _(u'Edit Link Portlet')


class Renderer(base.Renderer):

    def render(self):
        adapter = getMultiAdapter(
            (self.data, self.request, self), IPortletTemplate, name=self.data.template
        )
        return adapter.render()

    @property
    @memoize
    def items(self):
        infos = []
        return infos
