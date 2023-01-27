from zope.component import getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabulariesVocabulary:

    """Vocabulary for a list of available vocabulary factories"""

    def __call__(self, context):
        terms = []
        for name, vocabulary in getUtilitiesFor(IVocabularyFactory):
            doc = (vocabulary.__doc__ or "").strip().split("\n")
            doc = [item.strip() for item in doc if item.strip()]
            if len(doc) > 0:
                terms.append(SimpleTerm(name, name, f"{name} - {doc[0]}"))
            else:
                terms.append(SimpleTerm(name, name, name))

        terms = sorted(terms, key=lambda term: term.token)
        return SimpleVocabulary(terms)
