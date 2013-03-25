from zope import interface
from zope import schema
from plone import tiles


class IOEmbedTile(interface.Interface):
    """IOEmbed tile schema"""

    oembed_url = schema.URI(title=u"URL", required=True)

    maxwidth = schema.Int(title=u"max width", required=False)

    maxheight = schema.Int(title=u"Max height", required=False)

    responsive = schema.Bool(title=u"Responsive", required=True, default=True)


class OEmbedTile(tiles.PersistentTile):
    """OEmebed tile implementation"""

    interface.implements(IOEmbedTile)

    def get_embed(self):
        client = self.context.restrictedTraverse('@@proxy-oembed-provider')
#        client.update()

        maxwidth = self.data.get('maxwidth', None)
        maxheight = self.data.get('maxheight', None)

        return client.get_embed(self.data['oembed_url'], maxwidth=maxwidth,
                                maxheight=maxheight)
