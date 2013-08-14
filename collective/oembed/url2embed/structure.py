from collective.oembed.url2embed import gistgithub
from collective.oembed.url2embed import googlecalendar
from collective.oembed.url2embed import googledocs
from collective.oembed.url2embed import googlemaps
from collective.oembed.url2embed import issuucom
from collective.oembed.url2embed import itunes
from collective.oembed.url2embed import kinomap
from collective.oembed.url2embed import occipital360
from collective.oembed.url2embed import picasaweb
from collective.oembed.url2embed import scribd
from collective.oembed.url2embed import spotify


def endpoint_factory(info):
    return info['klass']()


class Consumer(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get_embed(self, url, maxwidth=None, maxheight=None):
        if self.endpoint is not None:
            return self.endpoint.get_embed(
                url,
                maxwidth=maxwidth,
                maxheight=maxheight
            )

    def get_embed_auto(self):
        url = self.context.getRemoteUrl()
        if self.endpoint is not None:
            return self.endpoint.get_embed(url)

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        if self.endpoint is not None:
            return self.endpoint.get_data(
                url,
                maxwidth=maxwidth,
                maxheight=maxheight
            )


def get_structure():
    structure = {}
    info = {
        'gist.github.com': (gistgithub.GistGithubURLEndPoint,),
        'www.google.com': (
            googlecalendar.GoogleCalendarURLEndPoint,
            googledocs.GoogleDocsURLEndPoint,
            googlemaps.GoogleMapsURLEndPoint
        ),
        'issuu.com': (issuucom.IssuuComEndPoint,),
        'itunes.apple.com': (itunes.ITunesURLEndPoint,),
        '360.io': (occipital360.Occipital360EndPoint,),
        'picasaweb.google.com': (picasaweb.PicasaWebURLEndPoint,),
        'www.scribd.com': (scribd.ScribdURLEndPoint,),
        'open.spotify.com': (spotify.SpotifyEndPoint,),
        'www.kinomap.com': (kinomap.KinomapEndPoint,),
    }
    for hostname in info:
        if hostname not in structure:
            structure[hostname] = []
        for endpoint in info[hostname]:
            structure[hostname].append({
                'factory': endpoint_factory,
                'consumer': Consumer,
                'klass': endpoint
            })

    return structure
