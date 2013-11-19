import json
import logging
from urlparse import urlparse
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from collective.oembed.consumer import ConsumerView
from Products.CMFCore.utils import getToolByName
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.app.textfield.interfaces import IRichText
from plone.namedfile.interfaces import INamedImageField
from zope.browser.interfaces import IBrowserView

logger = logging.getLogger('collective.oembed')


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
        self.updateFormat()
        self.updateInit()
        self.updateBuild()

    def updateFormat(self):
        if self.format is None:
            self.format = self.request.get('format', None)
        if self.format is None or not self.format:
            self.format = 'json'
        if self.format == 'json':
            self.request.response.setHeader('Content-Type', 'application/json')
        if self.format not in ('json', 'xml'):
            raise ValueError('format parameter must be in json, xml')

    def updateInit(self):
        if self.url is None:
            self.url = self.request.get('url', None)
        if self.url is None:
            raise KeyError('you must provide url parameter')
        if self.maxwidth is None:
            self.maxwidth = self.request.get('maxwidth', None)
        if self.maxheight is None:
            self.maxheight = self.request.get('maxheight', None)

    def updateBuild(self):
        if not self.url.startswith(self.context.absolute_url()):
            return
        path = self.get_path()
        site = self.get_site()
        if site is None or path is None:
            return
        ob = self.get_target()
        if ob is None:
            return
        self.build_info(ob, site)

    def build_info(self, context, site):
        site_title = site.Title()
        ob = context

        #site related info
        if type(site_title) != unicode:
            site_title = site_title.decode('utf-8')

        e = self.embed
        e[u'version'] = '1.0'
        e[u'author_url'] = site.absolute_url() + '/author/' + ob.Creator()
        e[u'provider_name'] = site_title
        e[u'provider_url'] = site.absolute_url()

        self.add_context_info(ob, site)

    def add_context_info(self, ob, site):
        """This help to build the context related information.
        As integrator you are supposed to overide this to support
        your specific use case.

        You must add information respecting the oembed specification
        You must store these information into self.embed dictionnary"""
        # context related info
        info = ob.restrictedTraverse("@@oembed-info")()
        self.embed.update(info)

    def render(self):
        if self.format == 'json':
            return json.dumps(self.embed)

        return self.index_xml()

    def get_path(self):
        parsed = urlparse(self.url)
        path = parsed.path
        return path

    def get_site(self):
        if self._site is None:
            urltool = getToolByName(self.context, 'portal_url')
            self._site = urltool.getPortalObject()
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
                # remove heading /
                self._target = site.restrictedTraverse(path[1:])
            except KeyError, e:
                logger.error('get_target error -> %s' % e)
                return

        if IBrowserView.providedBy(self._target):
            self._target = self._target.context

        return self._target


class ProxyOembedProvider(OEmbedProvider, ConsumerView):
    """This oembed provider can be used as proxy consumer"""
    def __init__(self, context, request):
        OEmbedProvider.__init__(self, context, request)
        ConsumerView.__init__(self, context, request)
        self.is_local = False

    def update(self):
        if self.url is None:
            self.url = self.request.get('url', None)

        OEmbedProvider.update(self)  # update in all case
        if self.url.startswith(self.context.absolute_url()):
            self.is_local = True
        else:
            ConsumerView.update(self)
            self._url = self.url
            self._maxheight = self.maxheight
            self._maxwidth = self.maxwidth

    def __call__(self):
        self.update()
        if self.is_local:
            result = OEmbedProvider.__call__(self)
        else:

            result = ConsumerView.get_data(
                self,
                self.url,
                maxwidth=self.maxwidth,
                maxheight=self.maxheight,
                format="json"
            )

            if type(result) == dict:
                result = json.dumps(result)

        return result


class DexterityOembedInfo(BrowserView):
    """optimized to work with plone.app.contenttypes"""
    def _getAuthorName(self):
        creator = self.context.Creator()
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(creator)
        if member is None:
            return creator
        return member.fullname

    def __call__(self):
        e = {}
        ob = self.context
        title = ob.Title()
        if type(title) != unicode:
            title.decode('utf-8')
        e[u'title'] = title
        e[u'author_name'] = self._getAuthorName()
        try:
            info = IPrimaryFieldInfo(ob)
        except TypeError:
            info = None
        if info is None:
            e[u'type'] = 'link'
        else:
            field = info.field
            if IRichText.providedBy(field):
                e[u'type'] = 'rich'
                e[u'html'] = info.value
            elif INamedImageField.providedBy(field):
                e[u'type'] = 'photo'
                e[u'url'] = ob.absolute_url()
                image = field.get(ob)
                e[u'width'], e['height'] = image.getImageSize()
            else:
                e[u'type'] = 'link'
        return e


class ArchetypesOembedInfo(BrowserView):
    def _getAuthorName(self):
        creator = self.context.Creator()
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getMemberById(creator)
        if member is None:
            return creator
        return member.fullname

    def __call__(self):
        e = {}
        ob = self.context
        title = ob.Title()
        if type(title) != unicode:
            title.decode('utf-8')
        e[u'title'] = title
        e[u'author_name'] = self._getAuthorName()
        field = ob.getPrimaryField()
        if field and field.type == 'text':
            e[u'type'] = 'rich'
            e[u'html'] = field.getAccessor(ob)()
        elif field and field.type == 'image':
            e[u'type'] = 'photo'
            e[u'url'] = ob.absolute_url()
            image = field.getAccessor(ob)()
            e[u'width'] = image.width
            e[u'height'] = image.height
        else:
            e[u'type'] = 'link'
        return e
