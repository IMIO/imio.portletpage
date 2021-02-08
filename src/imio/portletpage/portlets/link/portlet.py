# -*- coding: utf-8 -*-
from importlib.resources import is_resource, path
from plone import api
from plone import schema
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.app.portlets.portlets import base
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.interface import implementer

from imio.portletpage import _
from imio.portletpage.interfaces import IPortletTemplate


class ILinkPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Title"),
        required=True
    )

    # directives.widget(
    #     'content_uids',
    #     RelatedItemsFieldWidget,
    #     pattern_options={}
    # )
    # content_uids = schema.List(
    #     title=_(u"Items"),
    #     description=_(u"Select the items of you portlet"),
    #     required=True,
    #     value_type=schema.Choice(
    #         vocabulary='plone.app.vocabularies.Catalog',
    #     )
    # )

    template = schema.Choice(
        title=_(u"Template"),
        required=False,
        default=u"",
        vocabulary="imio.portletpage.PortletTemplates",
    )

    css_classes = schema.TextLine(
        title=_(u"CSS Classes"),
        description=_(u"CSS Classes to personnalize the portlet style"),
        required=False)


@implementer(ILinkPortlet)
class Assignment(base.Assignment):

    def __init__(self, header=u"", template=None, css_classes=u""):
        self.header = header
        self.template = template
        self.css_classes = css_classes

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
            (self.context, self.request), IPortletTemplate, name=self.data.template
        )
        return adapter.render()

    @property
    @memoize
    def items(self):
        infos = []
        return infos
