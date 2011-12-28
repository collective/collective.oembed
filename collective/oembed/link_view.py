from zope import component
from Products.Five.browser import BrowserView

from collective.oembed import interfaces
from collective.oembed import consumer

class LinkView(consumer.ConsumerView):
    """Link view with oembed rendering server side"""
    
