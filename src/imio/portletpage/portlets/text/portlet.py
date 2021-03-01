# -*- coding: utf-8 -*-
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import schema
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RichTextFieldWidget
from plone.app.portlets.portlets import base
from plone.autoform import directives
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer


class ITextPortlet(IPortletDataProvider):

    header = schema.TextLine(title=_(u"Title"), required=True)

    directives.widget(text=RichTextFieldWidget)
    text = RichText(
        title=_(u"Text"), description=_(u"The text to render"), required=True
    )

    css_classes = schema.TextLine(
        title=_(u"CSS Classes"),
        description=_(u"CSS Classes to personalise portlet"),
        required=False,
    )


@implementer(ITextPortlet)
class Assignment(base.Assignment):
    def __init__(self, header=u"", text=u"", css_classes=u""):
        self.header = header
        self.text = text
        self.css_classes = css_classes

    @property
    def title(self):
        return self.header


class AddForm(base.AddForm):
    schema = ITextPortlet
    label = _(u"Add Text Portlet")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = ITextPortlet
    label = _(u"Edit Text Portlet")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile("portlet.pt")
