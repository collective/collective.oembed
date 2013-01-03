from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.tiles.interfaces import ITile


@adapter(ITile, IObjectModifiedEvent)
def notifyModified(tile, event):
    # make sure the page's modified date gets updated
    tile.__parent__.notifyModified()
