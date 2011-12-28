from zope import interface
from zope import schema

from collective.oembed.i18n import messageFactory as _
from collective.oembed import vocabulary

class OEmbedLayer(interface.Interface):
    """browser layer for this addon"""

class IOEmbedClientSettings(interface.Interface):
    """Configuration of the jquery.oembed plugin. We are using it in implicit mode"""
    
    embedMethod = schema.Choice(title=_(u'embedMethod'),
                                description=_(u'embedMethod_description'),
                                vocabulary=vocabulary.embedMethods,
                                default=u'auto')

#    we will not using these options
#    maxWidth = schema.Int(title=_(u'maxWidth'),
#                          required=False)
#    
#    maxHeight = schema.Int(title=_(u'maxHeight'),
#                           required=False)

    defaultOEmbedProvider = schema.ASCIILine(title=_(u'defaultOEmbedProvider'),
                                             default="embed.ly")

    allowedProviders = schema.List(title=_(u'allowedProviders'),
                                   value_type=schema.ASCIILine(title=_(u'provider')),
                                   default=[],
                                   required=False)
    
    disallowedProviders = schema.List(title=_(u'disallowedProviders'),
                                   value_type=schema.ASCIILine(title=_(u'provider')),
                                   default=[],
                                   required=False)

    customProviders = schema.List(title=_(u'customProviders'),
                                  value_type=schema.ASCIILine(title=_(u'provider')),
                                  default=[],
                                   required=False)

    embedlykey = schema.ASCIILine(title=_(u'embedlykey'),
                                  required=False)
