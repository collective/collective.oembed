import json
from zope import interface
from zope import schema

from collective.oembed.i18n import messageFactory as _
from collective.oembed import vocabulary

class OEmbedLayer(interface.Interface):
    """browser layer for this addon"""


class IConsumer(interface.Interface):
    """consumer utility"""
    
    def get_data(url, maxwidth=None, maxheight=None, format='json'):
        """Return the data provided by the endpoint"""
    
    def embed(url, maxwidth=None, maxheight=None, format='json'):
        """Return the html code to display the content provided by url."""

class IOEmbedSettings(interface.Interface):
    """Client server side is named consumer"""
    
    embedly_apikey  = schema.ASCIILine(title=_(u'embedlykey'),
                                  required=False)
    
    activate_jqueryoembed_integration = schema.Bool(title=_(u"Activate jquery.oembed integration"),
                                                    description=_(u"If you have installed a jquery.oembed plugin, you can activate integration"),
                                                    default=False)

    #configuration for jquery.oembed javascript
    embedMethod = schema.Choice(title=_(u'embedMethod'),
                                description=_(u'embedMethod_description'),
                                vocabulary=vocabulary.embedMethods,
                                default=u'auto')

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
