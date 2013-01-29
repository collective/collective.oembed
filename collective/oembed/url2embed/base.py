from urlparse import urlsplit
from urllib import quote, urlencode
import oembed
from HTMLParser import HTMLParseError, HTMLParser
import urllib

DEFAULT_SIZE = 400


class UrlToOembed(oembed.OEmbedEndpoint):
    """URLEndpoint is able to build embed html snippet just from the URL.
    It is not able to get Title and description data.

    Child classes must define their own embeding template, as well as the
    request method to return the actual embeding code.
    """
    embed_html_template = """%(width)s%(height)s%(flashvar)s"""
    url_schemes = None
    oembed_type = ""

    def __init__(self):

        #Since classes derived from this one will deal with services
        #not supporting oEmbed, they won't need the provider's endpoint url
        super(UrlToOembed, self).__init__('', urlSchemes=self.url_schemes)

        #Stores urllib.urlencode() in a member var to avoid reimporting it
        #in child classes
        self._urlEncoder = urlencode
        self.embed = {}

    def break_url(self, url):
        """Beaks down the given url and returns each of its
        fragment to be processed by the caller
        """

        proto, host, path, query, fragment = urlsplit(url)
        path = quote(path)
        query = quote(query, safe='&=')
        fragment = quote(fragment, safe='')

        query_elems = {}
        # Put the query elems in a dict
        for pair in query.split('&'):
            pos = pair.find('=')
            if pos > -1:
                key = pair[:pos]
                value = pair[pos + 1:]
            else:
                key = pair
                value = ''
            if key:
                query_elems[key] = value

        return proto, host, path, query_elems, fragment

    def get_width_and_height(self, maxwidth=None, maxheight=None):
        """Sets the width & height params to a default value if they werent
        given.
        If only one param is given, then set the other one to same size.
        """

        if maxwidth is None:
            if maxheight is not None:
                maxwidth = maxheight
            else:
                if hasattr(self, 'default_width'):
                    maxwidth = self.default_width
                else:
                    maxwidth = DEFAULT_SIZE
                if hasattr(self, 'default_height'):
                    maxheight = self.default_height
                else:
                    maxheight = DEFAULT_SIZE
        elif maxheight is None:
                maxheight = maxwidth

        return maxwidth, maxheight

    def request(self, url):
        """Child classes must implement this method.

        Extract information from url needed by the template
        """
        raise NotImplementedError

    def get_embed(self, url, maxwidth=None, maxheight=None):
        """Build the embeding code from the given url according to the child
        class' template and return it
        """
        self.embed.update(self.request(url))
        w, h = self.get_width_and_height(maxwidth=maxwidth,
                                         maxheight=maxheight)

        self.embed['width'] = w
        self.embed['height'] = h
        return self.embed_html_template % self.embed

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        html = self.get_embed(url,
                              maxwidth=maxwidth,
                              maxheight=maxheight)
        e = self.embed
        e[u'version'] = '1.0'
        e[u'title'] = ""
        e[u'author_name'] = ""
        e[u'author_url'] = ""
        e[u'provider_name'] = ""
        e[u'provider_url'] = ""

        if self.oembed_type == "photo":
            e[u'type'] = 'photo'
            e[u'url'] = self.url
        elif self.oembed_type == "video":
            e[u'type'] = 'video'
            e[u'html'] = html
        elif self.oembed_type == "rich":
            e[u'type'] = 'rich'
            e[u'html'] = html
        else:
            e[u'type'] = 'link'

        return self.embed


class OembedHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []
        self.thumb = ""
        self.flashvar = ""
        self.description = ""
        self.title = ""
        self.width = ""
        self.height = ""
        self.type = ""
        self.audio = ""

    def has_finished(self):
        raise NotImplementedError()

    def update_data(self, data):
        for attr in ('title', 'width', 'height', 'type'):
            pvalue = getattr(self, attr)
            if pvalue:
                data[attr] = pvalue


class UrlCrawlerToEmbed(UrlToOembed):
    """This one read the page and extract data to generate the embed view"""

    parser_klass = None

    def __init__(self):
        super(UrlCrawlerToEmbed, self).__init__()
        self.parser = self.parser_klass()

    def parse(self, url):
        connection = urllib.urlopen(url)
        encoding = connection.headers.getparam('charset')
        u = connection.read().decode(encoding)

        lines = u.split("\n")

        for line in lines:
            if self.parser.has_finished():
                break
            try:
                if not line.strip().startswith('<'):
                    continue
                self.parser.feed(line)
            except HTMLParseError:
                continue

    def get_embed(self, url, maxwidth=None, maxheight=None):
        super(UrlCrawlerToEmbed, self).get_embed(
            url,
            maxwidth=maxwidth,
            maxheight=maxheight,
        )
        #lets override this one
        if self.parser.width:
            self.embed['width'] = self.parser.width
        if self.parser.height:
            self.embed['height'] = self.parser.height
        return self.embed_html_template % self.embed

    def get_data(self, url, maxwidth=None, maxheight=None, format="json"):
        super(UrlCrawlerToEmbed, self).get_data(
            url,
            maxwidth=maxwidth,
            maxheight=maxheight,
            format=format
        )
        self.parser.update_data(self.embed)
        return self.embed
