import logging
import oembed
from zope import interface
from collective.oembed import interfaces
from collective.oembed.embedly import EMBEDLY_RE
import urllib2

logger = logging.getLogger('collective.oembed')


TEMPLATES = {u"link": u"""
    <div class="oembed-wrapper oembed-link">
      <a href="%(url)s" target="_blank">%(title)s"></a>
      <div>%(html)s</div>
    </div>
    """,
             u"photo": u"""
    <div class="oembed-wrapper oembed-photo">
      <p><a href="%(url)s" target="_blank">%(title)s">
        <img src="%(url)s" alt="%(title)s"/>
      </a></p>
      <div>%(html)s</div>
    </div>
    """,
             u"rich": u"""
    <div class="oembed-wrapper oembed-rich">
      %(html)s
    </div>
    """,
             u"video": u"""
    <div class="oembed-wrapper oembed-video">
      %(html)s
    </div>
    """}


class Consumer(object):
    """Consumer which wrap one end point"""
    interface.implements(interfaces.IConsumer)

    def __init__(self, endpoint):
        self.consumer = None
        self.endpoint = endpoint

    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
        self.initialize_consumer()
        request = {}
        if maxwidth is not None:
            request['maxwidth'] = maxwidth
        if maxheight is not None:
            request['maxheight'] = maxheight
        request['format'] = format

        try:
            response = self.consumer.embed(url, **request)
            return response.getData()
        except oembed.OEmbedNoEndpoint, e:
            logger.info(e)
        except oembed.OEmbedError, e:
            #often a mimetype error
            logger.info(e)
        except urllib2.HTTPError, e:
            logger.info(e)
        except urllib2.URLError, e:
            #support offline mode
            logger.info('offline mode')

    def initialize_consumer(self):
        if self.consumer is None:

            consumer = oembed.OEmbedConsumer()
            consumer.addEndpoint(self.endpoint)

            self.consumer = consumer

    def get_embed(self, url, maxwidth=None, maxheight=None, format='json'):
        data = self.get_data(url, maxwidth=maxwidth, maxheight=maxheight,
                             format=format)
        if data is None or u"type" not in data:
            return u""
        return TEMPLATES[data[u"type"]] % data


REGEX_PROVIDERS = [
    {
        u'hostname': ('www.youtube.com',),
        u'regex': [
            'regex:.*youtube\.com/watch.*',
            'regex:.*youtube\.com/playlist.*'
        ],
        u'endpoint':'http://www.youtube.com/oembed',
    },
    {
        u'hostname': ('www.flickr.com',),
        u'regex': ['http://*.flickr.com/*'],
        u'endpoint':'http://www.flickr.com/services/oembed',
    },
    {
        u'hostname': ('qik.com',),
        u'regex': ['http://qik.com/video/*', 'http://qik.com/*'],
        u'endpoint':'http://qik.com/api/oembed.{format}',
    },
    {
        u'hostname': ('revision3.com',),
        u'regex': ['http://*revision3.com/*'],
        u'endpoint':'http://revision3.com/api/oembed/',
    },
    {
        u'hostname': ('www.hulu.com',),
        u'regex': ['http://www.hulu.com/watch/*'],
        u'endpoint':'http://www.hulu.com/api/oembed.{format}',
    },
    {
        u'hostname': ('vimeo.com',),
        u'regex': ['http://vimeo.com/*'],
        u'endpoint':'http://vimeo.com/api/oembed.{format}',
    },
    {
        u'hostname': ('www.collegehumor.com',),
        u'regex': ['http://www.collegehumor.com/video/*'],
        u'endpoint':'http://www.collegehumor.com/oembed.{format}',
    },
    {
        u'hostname': ('www.polleverywhere.com',),
        u'regex': ['http://www.polleverywhere.com/polls/*',
                   'http://www.polleverywhere.com/multiple_choice_polls/*',
                   'http://www.polleverywhere.com/free_text_polls/*'],
        u'endpoint':'http://www.polleverywhere.com/services/oembed/',
    },
    {
        u'hostname': ('www.ifixit.com',),
        u'regex': ['http://www.ifixit.com/*'],
        u'endpoint':'http://www.ifixit.com/Embed',
    },
    {
        u'hostname': ('smugmug.com', 'www.smugmug.com'),
        u'regex': ['http://*.smugmug.com/*'],
        u'endpoint':'http://api.smugmug.com/services/oembed/',
    },
    {
        u'hostname': ('www.slideshare.net', 'fr.slideshare.net'),
        u'regex': ['http://www.slideshare.net/*/*'],
        u'endpoint':'http://www.slideshare.net/api/oembed/2',
    },
    {
        u'hostname': ('www.23hq.com',),
        u'regex': ['http://www.23hq.com/*/photo/*'],
        u'endpoint':'http://www.23hq.com/23/oembed',
    },
    {
        u'hostname': ('www.5min.com',),
        u'regex': ['http://www.5min.com/Video/*'],
        u'endpoint':'http://api.5min.com/oembed.{format}',
    },
    {
        u'hostname': ('twitter.com',),
        u'regex': ['https://twitter.com/*/status*/*'],
        u'endpoint':'https://api.twitter.com/1/statuses/oembed.{format}',
    },
    {
        u'hostname': ('photobucket.com', 'img.photobucket.com'),
        #http://pic.pbsrc.com/dev_help/Metadata/Metadata_Discovery.htm
        u'regex': ['regex:.*photobucket\\.com/(albums|groups)/.+$'],
        u'endpoint':'http://photobucket.com/oembed',
    },
    {
        u'hostname': ('www.dailymotion.com',),
        #http://www.dailymotion.com/doc/api/oembed.html
        u'regex': ['http://www.dailymotion.com/video/*'],
        u'endpoint':'http://www.dailymotion.com/services/oembed',
    },
    {
        u'hostname': ('clikthrough.com', 'www.clikthrough.com'),
        u'regex': ['http://*.clikthrough.com/theater/video/*'],
        u'endpoint':'http://clikthrough.com/services/oembed',
    },
    {
        u'hostname': ('dotsub.com',),
        #http://solutions.dotsub.com/oEmbed
        u'regex': ['http://dotsub.com/view/*'],
        u'endpoint':'http://dotsub.com/services/oembed',
    },
    {
        u'hostname': ('blip.tv',),
        # blit.tv sends an invalid mime-type back
        u'regex': ['http://*blip.tv/*'],
        u'endpoint':'http://blip.tv/oembed/',
    },
    {
        u'hostname': ('official.fm',),
        #http://official.fm/developers/oembed
        u'regex': [
            'http://official.fm/tracks/*',
            'http://official.fm/playlists/*'
        ],
        u'endpoint':'http://official.fm/services/oembed.{format}',
    },
    {
        u'hostname': ('vhx.tv',),
        #http://dev.vhx.tv/oembed.html
        u'regex': ['http://vhx.tv/*'],
        u'endpoint':'http://vhx.tv/services/oembed.{format}',
    },
    {
        u'hostname': ('www.nfb.ca',),
        u'regex': ['http://*.nfb.ca/film/*'],
        u'endpoint':'http://www.nfb.ca/remote/services/oembed/',
    },
    {
        u'hostname': ('instagr.am', 'instagram.com'),
        #http://instagr.am/developer/embedding/
        u'regex': ['http://instagr.am/p/*', 'http://instagr.am/p/*'],
        u'endpoint': 'http://api.instagram.com/oembed',
    },
    {
        u'hostname': ('wordpress.tv',),
        u'regex': ['http://wordpress.tv/*'],
        u'endpoint': 'http://wordpress.tv/oembed/',
    },
    {
        u'hostname': ('soundcloud.com', 'snd.sc'),
        u'regex': [
            'http://soundcloud.com/*', 'http://soundcloud.com/*/*',
            'http://soundcloud.com/*/sets/*', 'http://soundcloud.com/groups/*',
            'http://snd.sc/*', 'https://soundcloud.com/*'
        ],
        u'endpoint': 'http://soundcloud.com/oembed',
    },
    {
        u'hostname': ('www.screenr.com',),
        #http://blog.screenr.com/post/2145539209/screenr-now-supports-oembed
        u'regex': ['http://www.screenr.com/*', 'http://screenr.com/*'],
        u'endpoint': 'http://www.screenr.com/api/oembed.{format}',
    },
]


class EmbedlyEndPoint(oembed.OEmbedEndpoint):
    """override this one to add api key"""

    def __init__(self, apikey):
        url = 'http://api.embed.ly/1/oembed'
        embedly_re = EMBEDLY_RE
        urlSchemes = [embedly_re]
        super(EmbedlyEndPoint, self).__init__(url, urlSchemes=urlSchemes)
        self.apikey = apikey

    def request(self, url, **opt):
        query = opt
        query['key'] = self.apikey
        return super(EmbedlyEndPoint, self).request(url, **query)


class WordpressEndPoint(oembed.OEmbedEndpoint):
    """Wordpress wait a for in his query params"""

    def __init__(self):
        url = 'http://public-api.wordpress.com/oembed/1.0/'
        urlSchemes = ['regex:.*.wordpress\.com/.*']
        super(WordpressEndPoint, self).__init__(url, urlSchemes=urlSchemes)

    def request(self, url, **opt):
        query = opt
        query['for'] = 'plone'
        return super(WordpressEndPoint, self).request(url, **query)


def wordpress_factory(info):
    return WordpressEndPoint()

#
#def load_all_endpoints(embedly_apikey=None):
#    endpoints = []
#    if embedly_apikey is not None:
#        endpoint = EmbedlyEndPoint(embedly_apikey)
#        endpoints.append(endpoint)
#
#    endpoint = WordpressEndPoint()
#    endpoints.append(endpoint)
#
#    providers = REGEX_PROVIDERS
#
#    for provider in providers:
#        endpoint = oembed.OEmbedEndpoint(provider[u'endpoint'],
#                                         provider[u'regex'])
#        endpoints.append(endpoint)
#
#    return endpoints


def endpoint_factory(info):
    return oembed.OEmbedEndpoint(info[u'endpoint'], info[u'regex'])


def get_structure():
    endpoints = {}

    for provider in REGEX_PROVIDERS:
        provider['factory'] = endpoint_factory
        provider['consumer'] = Consumer
        for hostname in provider['hostname']:
            endpoints[hostname] = [provider]

    return endpoints


def get_checkers():
    checkers = []
    wordpress = {
        'regex': '.*.wordpress\.com/.*',
        'factory': wordpress_factory,
        'consumer': Consumer
    }
    checkers.append(wordpress)
    return checkers
