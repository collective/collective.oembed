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
    
    def get_embed(url, maxwidth=None, maxheight=None, format='json'):
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

class IURL2Embed(interface.Interface):
    """To extend oembed experience we add a new kind of service: get the
    embed code directly from the URL. For example we can do that
    with picasaweb service. 
    
    Pros:
      * no need to request external service
    Cons:
      * we can't get external information like title, description, ...
    """

    embed_html_template = schema.ASCII(title=_(u"embed_html_template"))

    url_schemes = schema.List(title=_(u"url schemes"))

    def break_url(url):
        """utility which return proto, host, path, query, fragments
        """

    def get_embed(url, maxwidth=None, maxheight=None):
        """Return the embed html code build from embed_html_template using
        get_params_from_url"""

    def request(url):
        """Return a dict contains all needed params in embed_html_template
        except width and height, which are added by get_embed
        """

class IAPI2Embed(interface.Interface):
    """To extend oembed experience we add a new kind of service: get the 
    embed code using the API provided by the service. Implemented service
    are supposed to not providing oembed service.
    """

    def get_embed(url, maxwidth=None, maxheight=None):
        """Return the embed html code build from embed_html_template using
        get_params_from_url"""

    def get_data(url, maxwidth=None, maxheight=None):
        """Return a dict containing all information as a call on an embed
        service should have provided"""
