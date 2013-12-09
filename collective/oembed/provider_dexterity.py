from plone.app.textfield.interfaces import IRichText
from plone.namedfile.interfaces import INamedImageField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.CMFCore.utils import getToolByName


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
