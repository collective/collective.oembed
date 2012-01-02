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
        self.maxheight = None
        self.embed = {}
        
        self._site = None
        self._target = None

    
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
        if self.format is None:
            self.format = self.request.get('format',None)

        if self.format is None or not self.format:
            self.format = 'json'
        if self.format == 'json':
            self.request.response.setHeader('Content-Type','application/json')

        if self.format not in ('json','xml'):
            raise ValueError('format parameter must be in json, xml')

        if self.url is None:
            self.url = self.request.get('url',None)
        if self.url is None:
            raise KeyError('you must provide url parameter')

        if self.maxwidth is None:
            self.maxwidth = self.request.get('maxwidth',None)
        if self.maxheight is None:
            self.maxheight = self.request.get('maxheight',None)

        path = self.get_path()
        site = self.get_site()
        if site is None or path is None:
            return

        ob = self.get_target()
        if ob is None:
            return

        self.build_info(ob, site)

    def build_info(self, context, site):
        ob = context
        site_title = site.Title()

        title = ob.Title()
        if type(title) != unicode:
            title.decode('utf-8')
        if type(site_title) != unicode:
            site_title = site_title.decode('utf-8')


        e = self.embed
        e[u'version'] = '1.0'
        e[u'title'] = title
        e[u'author_name'] = ob.Creator()
        e[u'author_url'] = site.absolute_url()+'/author/' + ob.Creator()
        e[u'provider_name'] = site_title
        e[u'provider_url'] = site.absolute_url()
        if ob.portal_type == 'Image':
            e[u'type'] = 'photo'
            e[u'url'] = ob.absolute_url()
            image = ob.getField('image').get(ob)
            e[u'width'] = image.width
            e[u'height'] = image.height
        else:
            e[u'type'] = 'link'

    def render(self):
        res = self.embed
        if self.format == 'json':
            return json.dumps(res)

        return self.index_xml()

    def get_path(self):
        parsed = urlparse(self.url)
        path = parsed.path
        return path
    
    def get_site(self):
        if self._site is None:
            self._site = getSite()
        return self._site

    def get_target(self):
        site = self.get_site()
        path = self.get_path()
        portal_path = site.portal_url.getPortalPath()
        if path.startswith(portal_path):
            path = path[len(portal_path):]

        if site is None:
            return

        if self._target is None:
            try:
                self._target = site.restrictedTraverse(path[1:])#remove heading /
            except KeyError,e:
                logger.error(e)
                return

        return self._target
