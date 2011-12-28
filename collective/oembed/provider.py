import json
from urlparse import urlparse
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView

class OEmbedProvider(BrowserView):
    """OEmbed Provider"""
    
    index_xml = ViewPageTemplateFile('provider_xml.pt')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.format = None
        self.url = None
        self.maxwidth = None
        self.maxwidth = None
        self.embed = {}

    
    def __call__(self):
        try:
            self.update()
            return self.render()
        except KeyError, e:
            return e
        except ValueError, e:
            return e

    def update(self):
#        import pdb;pdb.set_trace()
        self.format = self.request.get('format',None)
        if self.format is None:
            self.format = 'json'
            self.request.response.setHeader('Content-Type','application/json')
        if self.format not in ('json','xml'):
            raise ValueError('format parameter must be in json, xml')
        self.url = self.request.get('url',None)
        if self.url is None:
            raise KeyError('you must provide url parameter')
        self.maxwidth = self.request.get('maxwidth',None)
        self.maxheight = self.request.get('maxheight',None)
        path = self.getPathFromURL()
        e = self.embed
        site = self.portal()
        ob = site.restrictedTraverse(path[1:]) #remove heading /
        e['version'] = '1.0'
        title = ob.Title()
        if type(title) != unicode:
            title.decode('utf-8')
        e['title'] = title
        e['author_name'] = ob.Creator()
        e['author_url'] = site.absolute_url()+'/author/' + ob.Creator()
        site_title = site.Title()
        if type(site_title) != unicode:
            site_title = site_title.decode('utf-8')
        e['provider_name'] = site_title
        e['provider_url'] = site.absolute_url()
        if ob.portal_type == 'Image':
            e['type'] = 'photo'
            e['url'] = ob.absolute_url()
            image = ob.getField('image').get(ob)
            e['width'] = image.width
            e['height'] = image.height
        else:
            e['type'] = 'link'

    def render(self):
        res = self.embed
        if self.format == 'json':
            return json.dumps(res)

        return self.index_xml()

    def getPathFromURL(self):
        parsed = urlparse(self.url)
        path = parsed.path
        return path
    
    def portal(self):
        return getSite()

