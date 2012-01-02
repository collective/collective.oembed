from collective.oembed.tests import base

class Test(base.UnitTestCase):
    
    def setUp(self):
        super(Test, self).setUp()
        from collective.oembed import consumer
        self.consumer = consumer.Consumer()

    def test_get_data(self):
        #test noendpoint exception, should return None
        url = 'http://notexisting.com/content'
        data = self.consumer.get_data(url)
        self.assertEqual(data, None)
        
        #test existing content
        url = 'http://www.youtube.com/watch?v=kHikGIWrvCs'
        data = self.consumer.get_data(url, maxwidth=300)
        self.failUnless(data is not None)
        self.failUnless(data[u'type']==u'video')
        self.failUnless(u'collective.oembed' in data[u'title'])
        self.failUnless(data[u'author_url']==u'http://www.youtube.com/user/toutpt')
        self.failUnless(data[u'html'].startswith(u'<iframe' ))
        self.failUnless(data[u'width'] == 300)

    def test_embed(self):
        url = 'http://www.youtube.com/watch?v=kHikGIWrvCs'
        embed = self.consumer.embed(url, maxwidth=310)
        self.failUnless(len(embed)>200) #quite some html code
        self.failUnless(type(embed)==unicode)
        self.failUnless(u"oembed-video" in embed)
        self.failUnless(u"oembed-wrapper" in embed)

    def test_initialize_consumer(self):
        self.failUnless(self.consumer.consumer is None)
        self.consumer.initialize_consumer()
        self.failUnless(self.consumer.consumer is not None)
        #check embedly
        endpoints_count = len(self.consumer.consumer.getEndpoints())
        self.consumer.consumer = None
        self.consumer.embedly_apikey = "123"
        self.consumer.initialize_consumer()
        endpoints_count2 = len(self.consumer.consumer.getEndpoints())
        self.failUnless(endpoints_count + 1 == endpoints_count2)

class TestIntegration(base.TestCase):

    def setUp(self):
        from zope import component
        from collective.oembed import consumer
        from collective.oembed.interfaces import IConsumer
        utility = component.queryUtility(IConsumer)
        self.utility = utility
        self.consumer_class = consumer.Consumer

    def test_get_consumer_utility(self):
        self.failUnless(self.utility is not None)
        self.failUnless(type(self.utility)==self.consumer_class)

    def test_endpoint_youtube(self):
        url = 'http://www.youtube.com/watch?v=kHikGIWrvCs'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]==u"video")

        url = 'http://www.youtube.com/playlist?list=PLF2CEDC7FD9EADDC5'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]==u"video")
        #TODO add wrong url and try do not matchin url

    def test_endpoint_flickr(self):
        url = 'http://www.flickr.com/photos/14516334@N00/345009210/'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        url_set = 'http://www.flickr.com/photos/dcplcommons/show'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_viddler(self):
        url = 'http://www.viddler.com/explore/37signals/videos/40/'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_qik(self):
        url = 'http://qik.com/video/46087949'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_revision3(self):
        url = 'http://revision3.com/askjay/profitsharing'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_hulu(self):
        url = 'http://www.hulu.com/watch/309602/family-guy-grumpy-old-man'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_slideshare(self):
        url = 'http://www.slideshare.net/irsan.element/merancang-hidup-by-irsan'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_vimeo(self):
        url = 'http://vimeo.com/20664159'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        #TODO add wrong url and try do not matchin url

    def test_endpoint_collegehumour(self):
        url_video = 'http://www.collegehumor.com/video/6664700/save-greendale-with-the-cast-of-community'
        data = self.utility.get_data(url_video)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]==u"video")

    def test_endpoint_polleverywhere(self):
        url = 'http://www.polleverywhere.com/multiple_choice_polls/LTIwNzM1NTczNTE'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]=="rich")
        #TODO add wrong url and try do not matchin url

    def test_endpoint_ifixit(self):
        url = 'http://www.ifixit.com/Teardown/iPhone-4-Teardown/3130/1'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]=="rich")
        #TODO add wrong url and try do not matchin url

    def test_endpoint_smugmug(self):
        url = 'http://www.smugmug.com/popular/all?125787395_hQSj9#125787395_hQSj9'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]=="photo")
        #TODO add wrong url and try do not matchin url

    def test_endpoint_wordpress(self):
        url = 'http://toutpt.wordpress.com/2011/02/10/collective-portlet-itemview/'
        data = self.utility.get_data(url)
        self.failUnless(data is not None)
        self.failUnless(data[u"type"]=="link",data[u"type"])

        #TODO add wrong url and try do not matchin url



def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    return base.build_test_suite((Test, TestIntegration))
