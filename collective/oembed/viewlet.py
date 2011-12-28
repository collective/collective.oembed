import json
import StringIO
from zope import component
from zope import schema
from plone.app.layout.viewlets import common

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
