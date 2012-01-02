Introduction
============

This addon integrate oembed_ into Plone. You can find a demo at
http://youtu.be/kHikGIWrvCs

ombed provider
==============

Your site will become oembed provider using @@oembed view as an endpoint::

    URL Scheme: http://mysite.com/*
    API endpoint: http://mysite.com/@@oembed
    Supports discovery via <link> tags

oembed client
=============

This addon provide an integration of jquery.oembed_ plugin. Because there are
many fork you have to choose the one you will use. The official plugin has been
integrated to plone throw the addon collective.js.oembed_

The oembed client is integrated using a viewlet that is not activated by
default. You have to activate it throw the controlpanel. It is configured that
way::

    <script type="text/javascript">
      jqueryOmebedSettings = {...} //extracted from the controlpanel
    </script>
    <script type="text/javascript">
            $(document).ready(function() {
                $(".oembed").oembed(null,jqueryOmebedSettings);
            });
    </script>

consumer
========

A consumer is availabe throw a utility::

    >>> url = "http://www.youtube.com/watch?v=it1hMtZKle8"
    >>> consumer = component.getUtility(collective.oembed.interfaces.IConsumer)
    >>> consumer.get_data(url, maxwidth=300, maxheight=None, format='json')
    {...}

There is also a @@collective.oembed.consumer view, which can take params throw
attributes::

    >>> consumer_view = component.queryMultiAdapter((self.context,self.request),
    ...                                 name=u'collective.oembed.consumer')
    >>> consumer_view._url = url
    >>> consumer_view.embed_auto()
    <div class="oembed-wrapper oembed-video">...</div>

OEmbed link view
================

This addon register an oembed view to the Link content type. It display 
content provided from the remote url and do not set maxwidth & maxheight. It
should be achieved by integrators.

Embed.ly
========

This addon can use embed.ly_ service. You can set the embed.ly api key in the
control panel or install and configure collective.embedly, this addon will
use the configuration provided by this one.

Providers
=========

embed.ly is activated only if you have added an api_key or configured 
collective.embedly. The addon provide native support for the following services:

External providers:

* Embedly (http://embed.ly)

Video providers:

* 5min (http://www.5min.com/)
* Youtube (http://www.youtube.com/)
* Viddler (http://www.viddler.com/)
* Qik (http://qik.com/)
* Revision3 (http://revision3.com/)
* Hulu (http://www.hulu.com/)
* Vimeo (http://vimeo.com/)
* CollegeHumor (http://www.collegehumor.com/)
* Kinomap (http://wwww.kinomap.com/)
* Dailymotion (http://www.dailymotion.com/)
* Clikthrough (http://clikthrough.com)
* Dotsub (http://dotsub.com/)

Photo providers:

* 23hq (http://www.23hq.com/)
* Flickr (http://www.flickr.com/)
* SmugMug (http://www.smugmug.com/)
* Photobucket (http://photobucket.com)
* Yfrog (http://yfrog.com/)

Rich providers:

* iFixit (http://www.iFixit.com)
* Poll Everywhere (http://www.polleverywhere.com/)
* SlideShare (http://www.slideshare.net/)
* WordPress (http://wordpress.com/)

Other Plone addons
==================

* collective.portlet.oembed_
* collective.js.oembed_
* collective.embedly_

Credits
=======

Companies
---------

|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_


Authors

  - JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

.. Contributors


.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _embed.ly: http://embed.ly
.. _oembed: http://oembed.com
.. _jquery.oembed: http://code.google.com/p/jquery-oembed/
.. _collective.portlet.oembed: http://pypi.python.org/pypi/collective.portlet.oembed
.. _collective.js.oembed: http://pypi.python.org/pypi/collective.js.oembed
.. _collective.embedly: http://pypi.python.org/pypi/collective.embedly
