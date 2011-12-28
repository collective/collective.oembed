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
        registry = component.getUtility(IRegistry)
        proxy = registry.forInterface(interfaces.IOEmbedClientSettings)
        #transform into json
        return proxy
    
    def settings_dict(self):
        res = {}
        proxy = self.settings()
        fields = schema.getFields(proxy.__schema__)

        for field in fields:
            value = getattr(proxy, field)
            if value is not None:
                res[field] = value

        return res

    def settings_json(self):
        sdict = self.settings_dict()
        return json.dumps(sdict)

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
        return u'%s oEmbed Profile'%self.context.Title()
