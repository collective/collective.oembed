import re
import logging

from datetime import datetime
from urlparse import urlsplit

from zope import interface

from collective.oembed.interfaces import IAPI2Embed

logger = logging.getLogger('collective.oembed')

TWITTER_EMBED = """<a class="embedly-card"
   width="300" height="500"
   href="%(url)s"
>Tweets by @%(username)s</a>
<script>!function(a){var b="embedly-platform",c="script";
if(!a.getElementById(b)){var d=a.createElement(c);
d.id=b,d.src=("https:"===document.location.protocol?"https":"http")+
"://cdn.embedly.com/widgets/platform.js";
var e=document.getElementsByTagName(c)[0];e.parentNode.insertBefore(d,e)}}
(document);
</script>
"""


class TwitterUserAPI2Embed(object):
    regex = '^https:\\/\\/twitter\\.com\\/([a-zA-Z0-9\\_]+)$'
    interface.implements(IAPI2Embed)

    def match(self, url):
        match = bool(re.match(self.regex, url))
        return match

    def get_embed(self, url, maxwidth=None, maxheight=None):
        info = self.get_info(url)
        if info is not None:
            return info['html']

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        return self.get_info(url)

#    @ram.cache(_get_tweets_cachekey)
    def get_info(self, url):
        username = urlsplit(url)[2][1:]

        oembed = {}
        e = oembed
        e[u'version'] = '1.0'
        e[u'title'] = username
        e[u'author_name'] = username
        e[u'author_url'] = url
        e[u'provider_name'] = "Plone"
        e[u'provider_url'] = "plone.org"
        e[u'type'] = 'rich'
        e[u'html'] = self.get_html(url)
        return oembed

    def update_time(self, tweet):
        time_format = '%a %b %d %H:%M:%S +0000 %Y'
        created_at = tweet['status']['created_at']
        created_at_dt = datetime.strptime(created_at, time_format)
        created_at_str = created_at_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        tweet['status']['created_at_datetime'] = created_at_str
        return tweet

    def get_html(self, url):
        return TWITTER_EMBED % {"url": url, "username": urlsplit(url)[2][1:]}
