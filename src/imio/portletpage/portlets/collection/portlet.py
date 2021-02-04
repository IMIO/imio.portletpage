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


class ICollectionPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Title"),
        required=True
    )

    directives.widget(
        'collection_uid',
        RelatedItemsFieldWidget,
        pattern_options={'selectableTypes': ['Collection']}
    )
    collection_uid = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to list"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
    )

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet."),
        required=True)

    # template = schema.Choice(
    #     title=_(u"Template"),
    #     required=False,
    #     default=u"",
    #     vocabulary='imio.portletpage.PortletCollectionTemplates')

    css_classes = schema.TextLine(
        title=_(u"CSS Classes"),
        description=_(u"CSS Classes to personnalize the portlet style"),
        required=False)


@implementer(ICollectionPortlet)
class Assignment(base.Assignment):

    def __init__(self, header=u"", collection_uid=None, limit=None, css_classes=u""):
        self.header = header
        self.collection_uid = collection_uid
        self.limit = limit
        self.css_classes = css_classes

    @property
    def title(self):
        return self.header


class AddForm(base.AddForm):
    schema = ICollectionPortlet
    label = _(u'Add Collection Portlet')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = ICollectionPortlet
    label = _(u'Edit Collection Portlet')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile("portlet.pt")

    @property
    @memoize
    def collection(self):
        return api.content.get(UID=self.data.collection_uid)

    @property
    @memoize
    def collection_url(self):
        return self.collection.absolute_url()

    @property
    @memoize
    def items(self):
        infos = []
        collection = self.collection
        limit = self.data.limit
        if collection is not None:
            brains = collection.queryCatalog(
                batch=True,
                b_size=limit
            )
            brains = brains._sequence  # TODO what is _sequence ?
            brains = brains[:limit]
            for b in brains:
                obj = b.getObject()
                infos.append({
                    'title': obj.title,
                    'description': obj.description if hasattr(obj, "description") else None,
                    'url': obj.remoteUrl  if hasattr(obj, "remoteUrl") else obj.absolute_url(),  # Use remoteUrl for Link content type
                    'image_url': obj.absolute_url() + "/@@images/image/preview" if (hasattr(obj, "image") and obj.image) else None,
                })
        return infos

