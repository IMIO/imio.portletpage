# -*- coding: utf-8 -*-

from imio.portletpage.interfaces import IPortletTemplate
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implementer
from zope.component import getAdapters


@implementer(IVocabularyFactory)
class PortletTemplateVocabularyFactory(object):
    """Vocabulary that list template available for portlets"""

    def __call__(self, context):
        # XXX Find a way to have the right context interface on add and edit portlet
        # form to allow only specific templates if necessary
        # context.REQUEST.PUBLISHED.schema return the schema from the current form view
        adapters = getAdapters((context, context.REQUEST, context), IPortletTemplate)
        # XXX The third parameter should be a mocked object because we don't have a 
        # renderer in add or edit form
        terms = []
        for name, adapter in adapters:
            terms.append(
                SimpleVocabulary.createTerm(name, name, adapter.title)
            )
        return SimpleVocabulary(terms)


PortletTemplateVocabulary = PortletTemplateVocabularyFactory()
