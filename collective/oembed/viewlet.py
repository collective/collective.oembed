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

    def __init__(self, context, request, view, manager=None):
        super(JQueryOEmbedViewlet, self).__init__(context, request, view, manager=None)
        self._settings = None
        self._fields = None

    def get_fields(self):
        if self._fields is None:
            proxy = self.settings()
            self._fields = schema.getFields(proxy.__schema__)
        return self._fields

    def settings(self):
        """Return settings"""

        if self._settings is None:
            registry = component.queryUtility(IRegistry)
            if registry is None:
                return
            try:
                self._settings = registry.forInterface(interfaces.IOEmbedSettings)
            except KeyError, e:
                pass

        return self._settings

    def settings_javascript(self):
        #this is not json, we need to serialize results in unicode manually
        proxy = self.settings()
        encoder = json.JSONEncoder()
        fields = self.get_fields()
        sio = StringIO.StringIO()
        sio.write(u"var %s = {"%self.jsvarname)

        for field in fields:
            value = getattr(proxy, field)
            if value is not None and value != []:
                sio.write(u'%s: %s,'%(field,encoder.encode(value)))
        value = sio.getvalue()

        return u'%s};'%(value[0:-1])

    def check_display_condition(self):
        settings = self.settings()
        if settings is None:
            return False
        try:
            return bool(settings.activate_jqueryoembed_integration)
        except AttributeError,e:
            return False

class Discovery(common.ViewletBase):
    """Add oembed discovery service"""

    index = ViewPageTemplateFile('viewlet-discovery.pt')
    
    def __init__(self, context, request, view, manager=None):
        super(Discovery, self).__init__(context, request, view, manager=None)
        self._query = None
        self._title = None

    def query(self):
        if self._query is None:
            self._query = {'url':self.context.absolute_url()}
        return self._query

    def oembed_url_json(self):
        query = self.query()
        query['format'] = 'json'
        return u'%s/@@oembed?%s'%(self.site_url, urllib.urlencode(query))
    
    def oembed_url_xml(self):
        query = self.query()
        query['format'] = 'xml'
        return u'%s/@@oembed?%s'%(self.site_url, urllib.urlencode(query))
    
    def title(self):
        if self._title is None:
            self._title = u'%s oEmbed Profile'%self.context.Title().decode('utf-8')
        return self._title
