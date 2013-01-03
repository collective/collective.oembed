from zope import component
from zope import interface
from zope import schema
from plone import tiles
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IOEmbedTile(interface.Interface):
    """IOEmbed tile schema"""

    oembed_url = schema.URI(title=u"URL",
                     required=True)

    maxwidth = schema.Int(title=u"max width",
                          required=False)

    maxheight = schema.Int(title=u"Max height",
                           required=False)


class OEmbedTile(tiles.PersistentTile):
    """OEmebed tile implementation"""

    interface.implements(IOEmbedTile)

    def __call__(self):
        embed = self.get_embed()
        if not embed:
            embed = '&nbsp;'
        return '<html><body>%s</body></html>' % embed

    def get_embed(self):
        client = component.queryMultiAdapter((self.context, self.request),
                                    name=u"collective.oembed.superconsumer")
        client.update()

        maxwidth = self.data.get('maxwidth', None)
        maxheight = self.data.get('maxheight', None)

        return client.get_embed(self.data['oembed_url'], maxwidth=maxwidth,
                                maxheight=maxheight)
