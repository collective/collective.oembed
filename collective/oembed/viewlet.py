import json
import StringIO
import urllib
from zope import component
from zope import schema
from plone.app.layout.viewlets import common

from plone.memoize.instance import memoize
from collective.oembed import interfaces
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class JQueryOEmbedViewlet(common.ViewletBase):
    """This viewlet configure and activate jquery.oembed script"""
    
    index = ViewPageTemplateFile('viewlet-jquery-oembed.pt')
    jsvarname = u'jqueryOmebedSettings'

    def settings(self):
        """Return settings"""
        registry = component.queryUtility(IRegistry)
        if registry is None:
            return
        try:
            proxy = registry.forInterface(interfaces.IOEmbedSettings)
            return proxy
        except KeyError, e:
            pass

    def settings_javascript(self):
        #this is not json, we need to serialize results in unicode by hand
        proxy = self.settings()
        encoder = json.JSONEncoder()
        fields = schema.getFields(proxy.__schema__)
        sio = StringIO.StringIO()
        sio.write(u"var %s = {"%self.jsvarname)

        for field in fields:
            value = getattr(proxy, field)
            if value is not None and value != []:
                sio.write(u'%s: %s,'%(field,encoder.encode(value)))
        value = sio.getvalue()

        return u'%s};'%(value[0:-1])

    def display_condition(self):
        settings = self.settings
        if settings is None:
            return False
        try:
            return bool(settings.activate_jqueryoembed_integration)
        except AttributeError,e:
            return False

class Discovery(common.ViewletBase):
    """Add oembed discovery service"""

    index = ViewPageTemplateFile('viewlet-discovery.pt')

    @memoize
    def query(self):
        query = {'url':self.context.absolute_url()}
        return query

    def oembed_url_json(self):
        query = self.query()
        query['format'] = 'json'
        return u'%s?%s'%(self.site_url, urllib.urlencode(query))
    
    def oembed_url_xml(self):
        query = self.query()
        query['format'] = 'xml'
        return u'%s?%s'%(self.site_url, urllib.urlencode(query))
    
    @memoize
    def title(self):
        return u'%s oEmbed Profile'%self.context.Title().decode('utf-8')
