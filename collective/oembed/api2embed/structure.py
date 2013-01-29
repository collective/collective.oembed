from collective.oembed.api2embed import twitteruser


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
        'twitter.com': (twitteruser.TwitterUserAPI2Embed,),
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
