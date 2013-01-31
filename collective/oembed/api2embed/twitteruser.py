import re
import json
import urllib
import logging

from datetime import datetime
from urlparse import urlsplit

from zope import interface

from collective.oembed.interfaces import IAPI2Embed

logger = logging.getLogger('collective.oembed')

TWITTER_EMBED = """<blockquote class="twitter-tweet">
<p>%(tweet)s</p>&mdash; %(name)s (@%(screen_name)s)
<a href="%(tweet_url)s" data-datetime="%(datetime)s">%(human_datetime)s</a>
</blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
"""


class TwitterUserAPI2Embed(object):
    regex = '^https:\\/\\/twitter\\.com\\/([a-zA-Z0-9\\_]+)$'
    interface.implements(IAPI2Embed)

    def match(self, url):
        return bool(re.match(self.regex, url))

    def get_embed(self, url, maxwidth=None, maxheight=None):
        info = self.get_info(url)
        if info is not None:
            return info['html']

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        return self.get_info(url)

#    @ram.cache(_get_tweets_cachekey)
    def get_info(self, url):
        get_url = "https://twitter.com/users/%s.json"
        proto, host, path, query, fragment = urlsplit(url)

        account_url = get_url % path[1:]
        account_info = None

        try:
            account_info = json.loads(urllib.urlopen(account_url).read())
            if "errors" in account_info:
                logger.error(account_info['errors'])
                return
            if 'status' in account_info:
                self.update_time(account_info)
        except IOError, e:
            logger.error(e)
            return
        oembed = {}
        e = oembed
        e[u'version'] = '1.0'
        e[u'title'] = account_info['name']
        e[u'author_name'] = account_info['name']
        e[u'author_url'] = url
        e[u'provider_name'] = "Plone"
        e[u'provider_url'] = "plone.org"
        e[u'type'] = 'rich'
        e[u'html'] = self.get_html(account_info)
        return oembed

    def update_time(self, tweet):
        time_format = '%a %b %d %H:%M:%S +0000 %Y'
        created_at = tweet['status']['created_at']
        created_at_dt = datetime.strptime(created_at, time_format)
        created_at_str = created_at_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        tweet['status']['created_at_datetime'] = created_at_str
        return tweet

    def get_html(self, info):
        if 'status' not in info:
            return u''
        url = "https://twitter.com/%s/status/%s" % (info['screen_name'],
                                                    info['status']['id_str'])
        template_info = {'tweet': info['status']['text'],
                         'tweet_url': url,
                         'name': info['name'],
                         'screen_name': info['screen_name'],
                         'datetime': info['status']['created_at_datetime'],
                         'human_datetime': info['status']['created_at']}
        return TWITTER_EMBED % template_info
