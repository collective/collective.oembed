from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.oembed.i18n import messageFactory as _

embedMethods = SimpleVocabulary(
    [SimpleTerm(value=u'append',  title=_(u'append')),
     SimpleTerm(value=u'fill',    title=_(u'fill')),
     SimpleTerm(value=u'replace', title=_(u'replace')),
     SimpleTerm(value=u'auto', title=_(u'auto'))]
    )

