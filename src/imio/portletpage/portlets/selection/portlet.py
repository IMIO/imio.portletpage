# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.portletpage import _
from imio.portletpage.interfaces import IPortletTemplate
from importlib.resources import is_resource, path
from plone import api
from plone import schema
from plone.app.portlets.portlets import base
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.autoform import directives
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.interface import implementer


class ISelectionPortlet(IPortletDataProvider):

    header = schema.TextLine(title=_(u"Title"), required=True)

    directives.widget("content_uids", RelatedItemsFieldWidget, pattern_options={})
    content_uids = schema.List(
        title=_(u"Items"),
        description=_(u"Select the items of you portlet"),
        required=True,
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Catalog"),
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


@implementer(ISelectionPortlet)
class Assignment(base.Assignment):
    def __init__(self, header=u"", content_uids=[], css_classes=u"", template=None):
        self.header = header
        self.content_uids = content_uids
        self.css_classes = css_classes
        self.template = template

    @property
    def title(self):
        return self.header


class AddForm(base.AddForm):
    schema = ISelectionPortlet
    label = _(u"Add Selection Portlet")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = ISelectionPortlet
    label = _(u"Edit Selection Portlet")


class Renderer(base.Renderer):
    def render(self):
        adapter = getMultiAdapter(
            (self.context, self.request), IPortletTemplate, name=self.data.template
        )
        return adapter.render()

    @property
    @memoize
    def contents(self):
        return [api.content.get(UID=uid) for uid in self.data.content_uids]

    @property
    @memoize
    def items(self):
        infos = []
        for obj in self.contents:
            infos.append(
                {
                    "title": obj.title,
                    "description": obj.description
                    if hasattr(obj, "description")
                    else None,
                    "url": obj.remoteUrl
                    if hasattr(obj, "remoteUrl")
                    else obj.absolute_url(),  # Use remoteUrl for Link content type
                    "image_url": obj.absolute_url() + "/@@images/image/preview"
                    if (hasattr(obj, "image") and obj.image)
                    else None,
                }
            )
        return infos
