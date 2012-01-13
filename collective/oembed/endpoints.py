import oembed

REGEX_PROVIDERS = [
 {u'regex': ['regex:.*youtube\.com/watch.*','regex:.*youtube\.com/playlist.*'],
  u'endpoint':'http://www.youtube.com/oembed'},
 {u'regex':['http://*.flickr.com/*'],
  u'endpoint':'http://www.flickr.com/services/oembed'},
 {u'regex':['http://qik.com/video/*','http://qik.com/*'],
  u'endpoint':'http://qik.com/api/oembed.{format}'},
 {u'regex':['http://*revision3.com/*'],
  u'endpoint':'http://revision3.com/api/oembed/'},
 {u'regex':['http://www.hulu.com/watch/*'],
  u'endpoint':'http://www.hulu.com/api/oembed.{format}'},
 {u'regex':['http://vimeo.com/*'],
  u'endpoint':'http://vimeo.com/api/oembed.{format}'},
 {u'regex':['http://www.collegehumor.com/video/*'],
  u'endpoint':'http://www.collegehumor.com/oembed.{format}'},
 {u'regex':['http://www.polleverywhere.com/polls/*','http://www.polleverywhere.com/multiple_choice_polls/*','http://www.polleverywhere.com/free_text_polls/*'],
  u'endpoint':'http://www.polleverywhere.com/services/oembed/'},
 {u'regex':['http://www.ifixit.com/*'],
  u'endpoint':'http://www.ifixit.com/Embed'},
 {u'regex':['http://*.smugmug.com/*'],
  u'endpoint':'http://api.smugmug.com/services/oembed/'},
 {u'regex':['http://www.slideshare.net/*/*'],
  u'endpoint':'http://www.slideshare.net/api/oembed/2'},
 {u'regex':['http://www.23hq.com/*/photo/*'],
  u'endpoint':'http://www.23hq.com/23/oembed'},
 {u'regex':['http://www.5min.com/Video/*'],
  u'endpoint':'http://api.5min.com/oembed.{format}'}, #http://www.5min.com/APIDocs/Embed.aspx
 {u'regex':['https://twitter.com/*/status*/*'],
  u'endpoint':'https://api.twitter.com/1/statuses/oembed.{format}'}, #https://dev.twitter.com/docs/embedded-tweets
 {u'regex':['regex:.*photobucket\\.com/(albums|groups)/.+$'],
  u'endpoint':'http://photobucket.com/oembed'}, #http://pic.pbsrc.com/dev_help/Metadata/Metadata_Discovery.htm
 {u'regex':['http://*.kinomap.com/*'],
  u'endpoint':'http://www.kinomap.com/oembed'}, #http://pic.pbsrc.com/dev_help/Metadata/Metadata_Discovery.htm
 {u'regex':['http://www.dailymotion.com/video/*'],
  u'endpoint':'http://www.dailymotion.com/services/oembed'}, #http://www.dailymotion.com/doc/api/oembed.html
 {u'regex':['http://*.clikthrough.com/theater/video/*'],
  u'endpoint':'http://clikthrough.com/services/oembed'},
 {u'regex':['http://dotsub.com/view/*'],
  u'endpoint':'http://dotsub.com/services/oembed'}, #http://solutions.dotsub.com/oEmbed
 {u'regex':['http://*blip.tv/*'],              # blit.tv sends an invalid mime-type back
  u'endpoint':'http://blip.tv/oembed/'},
 {u'regex':['http://official.fm/tracks/*', 'http://official.fm/playlists/*'],
  u'endpoint':'http://official.fm/services/oembed.{format}'}, #http://official.fm/developers/oembed
 {u'regex':['http://vhx.tv/*'], #http://dev.vhx.tv/oembed.html
  u'endpoint':'http://vhx.tv/services/oembed.{format}'},
 {u'regex':['http://*.nfb.ca/film/*'],
  u'endpoint':'http://www.nfb.ca/remote/services/oembed/'},
 {u'regex':['http://instagr.am/p/*', 'http://instagr.am/p/*'], #http://instagr.am/developer/embedding/
  u'endpoint':'http://api.instagram.com/oembed'},
 {u'regex':['http://wordpress.tv/*'],
  u'endpoint':'http://wordpress.tv/oembed/'},
#
# Those features don't work currently, but are being worked upon:
#
#
# {u'regex':['http://*.viddler.com/*'],
#  u'endpoint':'http://lab.viddler.com/services/oembed/'},
#
# {u'regex':['http://*yfrog.com/*'],
#  u'endpoint':'http://www.yfrog.com/api/oembed'}, #http://yfrog.com/page/api#a8
#
# {u'regex':['/vz.net\/Profile/.*/', '/vz.net\/Groups/Overview/.*/', '/vz.net\/l/.*/', '/vz.net\/Gadgets/Info/.*/', '/vz.net\/Gadgets/Install/.*/',
#'/meinvz.net\/[a-zA-Z0-9\-\_]*$/', '/studivz.net\/[a-zA-Z0-9\-\_]*$/', '/schuelervz.net\/[a-zA-Z0-9\-\_]*$/'],
#  u'endpoint':'http://www.studivz.net/Link/OEmbed/'}, #http://developer.studivz.net/wiki/index.php/Embedding#List_of_white-listed_services
#
# {u'regex':['http://*.deviantart.com/art/*', 'http://fav.me/*', 'http://*.deviantart.com/*#/d*'],
#  u'endpoint':'http://backend.deviantart.com/oembed'}, #http://www.deviantart.com/developers/oembed
#
# {u'regex':['http://*.scribd.com/*'],
#  u'endpoint':'http://www.scribd.com/services/oembed'},
#
# {u'regex':['http://*funnyordie.com/videos/*'],
#  u'endpoint':'http://www.funnyordie.com/oembed'}, 
#
# {u'regex':['http://my.opera.com/*'],
#  u'endpoint':'http://my.opera.com/service/oembed'}, #http://my.opera.com/devblog/blog/2008/12/02/embedding-my-opera-content-oembed
# {u'regex':['http://tv.majorleaguegaming.com/video/*', 'http://mlg.tv/video/*'],
#  u'endpoint':'http://tv.majorleaguegaming.com/oembed'},
]

class EmbedlyEndPoint(oembed.OEmbedEndpoint):
    """override this one to add api key"""

    def __init__(self, apikey):
        url = 'http://api.embed.ly/1/oembed'
        embedly_re = 'regex:((http://(.*yfrog\..*/.*|twitter\.com/.*/status/.*/photo/.*|twitter\.com/.*/statuses/.*/photo|pic\.twitter\.com/.*|www\.twitter\.com/.*/statuses/.*/photo/.*|mobile\.twitter\.com/.*/status/.*/photo/.*|mobile\.twitter\.com/.*/statuses/.*/photo/.*|www\.flickr\.com/photos/.*|flic\.kr/.*|twitpic\.com/.*|www\.twitpic\.com/.*|twitpic\.com/photos/.*|www\.twitpic\.com/photos/.*|.*imgur\.com/.*|.*\.posterous\.com/.*|post\.ly/.*|twitgoo\.com/.*|i.*\.photobucket\.com/albums/.*|s.*\.photobucket\.com/albums/.*|media\.photobucket\.com/image/.*|phodroid\.com/.*/.*/.*|www\.mobypicture\.com/user/.*/view/.*|moby\.to/.*|xkcd\.com/.*|www\.xkcd\.com/.*|imgs\.xkcd\.com/.*|www\.asofterworld\.com/index\.php\?id=.*|www\.asofterworld\.com/.*\.jpg|asofterworld\.com/.*\.jpg|www\.qwantz\.com/index\.php\?comic=.*|23hq\.com/.*/photo/.*|www\.23hq\.com/.*/photo/.*|.*dribbble\.com/shots/.*|drbl\.in/.*|.*\.smugmug\.com/.*|.*\.smugmug\.com/.*#.*|emberapp\.com/.*/images/.*|emberapp\.com/.*/images/.*/sizes/.*|emberapp\.com/.*/collections/.*/.*|emberapp\.com/.*/categories/.*/.*/.*|embr\.it/.*|picasaweb\.google\.com.*/.*/.*#.*|picasaweb\.google\.com.*/lh/photo/.*|picasaweb\.google\.com.*/.*/.*|dailybooth\.com/.*/.*|brizzly\.com/pic/.*|pics\.brizzly\.com/.*\.jpg|img\.ly/.*|www\.tinypic\.com/view\.php.*|tinypic\.com/view\.php.*|www\.tinypic\.com/player\.php.*|tinypic\.com/player\.php.*|www\.tinypic\.com/r/.*/.*|tinypic\.com/r/.*/.*|.*\.tinypic\.com/.*\.jpg|.*\.tinypic\.com/.*\.png|meadd\.com/.*/.*|meadd\.com/.*|.*\.deviantart\.com/art/.*|.*\.deviantart\.com/gallery/.*|.*\.deviantart\.com/#/.*|fav\.me/.*|.*\.deviantart\.com|.*\.deviantart\.com/gallery|.*\.deviantart\.com/.*/.*\.jpg|.*\.deviantart\.com/.*/.*\.gif|.*\.deviantart\.net/.*/.*\.jpg|.*\.deviantart\.net/.*/.*\.gif|www\.fotopedia\.com/.*/.*|fotopedia\.com/.*/.*|photozou\.jp/photo/show/.*/.*|photozou\.jp/photo/photo_only/.*/.*|instagr\.am/p/.*|instagram\.com/p/.*|skitch\.com/.*/.*/.*|img\.skitch\.com/.*|share\.ovi\.com/media/.*/.*|www\.questionablecontent\.net/|questionablecontent\.net/|www\.questionablecontent\.net/view\.php.*|questionablecontent\.net/view\.php.*|questionablecontent\.net/comics/.*\.png|www\.questionablecontent\.net/comics/.*\.png|picplz\.com/.*|twitrpix\.com/.*|.*\.twitrpix\.com/.*|www\.someecards\.com/.*/.*|someecards\.com/.*/.*|some\.ly/.*|www\.some\.ly/.*|pikchur\.com/.*|achewood\.com/.*|www\.achewood\.com/.*|achewood\.com/index\.php.*|www\.achewood\.com/index\.php.*|www\.whosay\.com/content/.*|www\.whosay\.com/photos/.*|www\.whosay\.com/videos/.*|say\.ly/.*|ow\.ly/i/.*|color\.com/s/.*|bnter\.com/convo/.*|mlkshk\.com/p/.*|lockerz\.com/s/.*|lightbox\.com/.*|www\.lightbox\.com/.*|soundcloud\.com/.*|soundcloud\.com/.*/.*|soundcloud\.com/.*/sets/.*|soundcloud\.com/groups/.*|snd\.sc/.*|www\.last\.fm/music/.*|www\.last\.fm/music/+videos/.*|www\.last\.fm/music/+images/.*|www\.last\.fm/music/.*/_/.*|www\.last\.fm/music/.*/.*|www\.mixcloud\.com/.*/.*/|www\.radionomy\.com/.*/radio/.*|radionomy\.com/.*/radio/.*|www\.hark\.com/clips/.*|www\.rdio\.com/#/artist/.*/album/.*|www\.rdio\.com/artist/.*/album/.*|www\.zero-inch\.com/.*|.*\.bandcamp\.com/|.*\.bandcamp\.com/track/.*|.*\.bandcamp\.com/album/.*|freemusicarchive\.org/music/.*|www\.freemusicarchive\.org/music/.*|freemusicarchive\.org/curator/.*|www\.freemusicarchive\.org/curator/.*|www\.npr\.org/.*/.*/.*/.*/.*|www\.npr\.org/.*/.*/.*/.*/.*/.*|www\.npr\.org/.*/.*/.*/.*/.*/.*/.*|www\.npr\.org/templates/story/story\.php.*|huffduffer\.com/.*/.*|www\.audioboo\.fm/boos/.*|audioboo\.fm/boos/.*|boo\.fm/b.*|www\.xiami\.com/song/.*|xiami\.com/song/.*|www\.saynow\.com/playMsg\.html.*|www\.saynow\.com/playMsg\.html.*|grooveshark\.com/.*|radioreddit\.com/songs.*|www\.radioreddit\.com/songs.*|radioreddit\.com/\?q=songs.*|www\.radioreddit\.com/\?q=songs.*|www\.gogoyoko\.com/song/.*|.*amazon\..*/gp/product/.*|.*amazon\..*/.*/dp/.*|.*amazon\..*/dp/.*|.*amazon\..*/o/ASIN/.*|.*amazon\..*/gp/offer-listing/.*|.*amazon\..*/.*/ASIN/.*|.*amazon\..*/gp/product/images/.*|.*amazon\..*/gp/aw/d/.*|www\.amzn\.com/.*|amzn\.com/.*|www\.shopstyle\.com/browse.*|www\.shopstyle\.com/action/apiVisitRetailer.*|api\.shopstyle\.com/action/apiVisitRetailer.*|www\.shopstyle\.com/action/viewLook.*|itunes\.apple\.com/.*|gist\.github\.com/.*|twitter\.com/.*/status/.*|twitter\.com/.*/statuses/.*|www\.twitter\.com/.*/status/.*|www\.twitter\.com/.*/statuses/.*|mobile\.twitter\.com/.*/status/.*|mobile\.twitter\.com/.*/statuses/.*|www\.crunchbase\.com/.*/.*|crunchbase\.com/.*/.*|www\.slideshare\.net/.*/.*|www\.slideshare\.net/mobile/.*/.*|slidesha\.re/.*|scribd\.com/doc/.*|www\.scribd\.com/doc/.*|scribd\.com/mobile/documents/.*|www\.scribd\.com/mobile/documents/.*|screenr\.com/.*|polldaddy\.com/community/poll/.*|polldaddy\.com/poll/.*|answers\.polldaddy\.com/poll/.*|www\.5min\.com/Video/.*|www\.howcast\.com/videos/.*|www\.screencast\.com/.*/media/.*|screencast\.com/.*/media/.*|www\.screencast\.com/t/.*|screencast\.com/t/.*|issuu\.com/.*/docs/.*|www\.kickstarter\.com/projects/.*/.*|www\.scrapblog\.com/viewer/viewer\.aspx.*|foursquare\.com/.*|www\.foursquare\.com/.*|4sq\.com/.*|ping\.fm/p/.*|chart\.ly/symbols/.*|chart\.ly/.*|maps\.google\.com/maps\?.*|maps\.google\.com/\?.*|maps\.google\.com/maps/ms\?.*|.*\.craigslist\.org/.*/.*|my\.opera\.com/.*/albums/show\.dml\?id=.*|my\.opera\.com/.*/albums/showpic\.dml\?album=.*&picture=.*|tumblr\.com/.*|.*\.tumblr\.com/post/.*|www\.polleverywhere\.com/polls/.*|www\.polleverywhere\.com/multiple_choice_polls/.*|www\.polleverywhere\.com/free_text_polls/.*|www\.quantcast\.com/wd:.*|www\.quantcast\.com/.*|siteanalytics\.compete\.com/.*|statsheet\.com/statplot/charts/.*/.*/.*/.*|statsheet\.com/statplot/charts/e/.*|statsheet\.com/.*/teams/.*/.*|statsheet\.com/tools/chartlets\?chart=.*|.*\.status\.net/notice/.*|identi\.ca/notice/.*|brainbird\.net/notice/.*|shitmydadsays\.com/notice/.*|www\.studivz\.net/Profile/.*|www\.studivz\.net/l/.*|www\.studivz\.net/Groups/Overview/.*|www\.studivz\.net/Gadgets/Info/.*|www\.studivz\.net/Gadgets/Install/.*|www\.studivz\.net/.*|www\.meinvz\.net/Profile/.*|www\.meinvz\.net/l/.*|www\.meinvz\.net/Groups/Overview/.*|www\.meinvz\.net/Gadgets/Info/.*|www\.meinvz\.net/Gadgets/Install/.*|www\.meinvz\.net/.*|www\.schuelervz\.net/Profile/.*|www\.schuelervz\.net/l/.*|www\.schuelervz\.net/Groups/Overview/.*|www\.schuelervz\.net/Gadgets/Info/.*|www\.schuelervz\.net/Gadgets/Install/.*|www\.schuelervz\.net/.*|myloc\.me/.*|pastebin\.com/.*|pastie\.org/.*|www\.pastie\.org/.*|redux\.com/stream/item/.*/.*|redux\.com/f/.*/.*|www\.redux\.com/stream/item/.*/.*|www\.redux\.com/f/.*/.*|cl\.ly/.*|cl\.ly/.*/content|speakerdeck\.com/u/.*/p/.*|www\.kiva\.org/lend/.*|www\.timetoast\.com/timelines/.*|storify\.com/.*/.*|.*meetup\.com/.*|meetu\.ps/.*|www\.dailymile\.com/people/.*/entries/.*|.*\.kinomap\.com/.*|www\.metacdn\.com/r/c/.*/.*|www\.metacdn\.com/r/m/.*/.*|prezi\.com/.*/.*|.*\.uservoice\.com/.*/suggestions/.*|formspring\.me/.*|www\.formspring\.me/.*|formspring\.me/.*/q/.*|www\.formspring\.me/.*/q/.*|twitlonger\.com/show/.*|www\.twitlonger\.com/show/.*|tl\.gd/.*|www\.qwiki\.com/q/.*|crocodoc\.com/.*|.*\.crocodoc\.com/.*|www\.wikipedia\.org/wiki/.*|www\.wikimedia\.org/wiki/File.*|graphicly\.com/.*/.*/.*|.*youtube\.com/watch.*|.*\.youtube\.com/v/.*|youtu\.be/.*|.*\.youtube\.com/user/.*|.*\.youtube\.com/.*#.*/.*|m\.youtube\.com/watch.*|m\.youtube\.com/index.*|.*\.youtube\.com/profile.*|.*\.youtube\.com/view_play_list.*|.*\.youtube\.com/playlist.*|.*twitch\.tv/.*|.*justin\.tv/.*/b/.*|.*justin\.tv/.*/w/.*|.*twitch\.tv/.*|.*twitch\.tv/.*/b/.*|www\.ustream\.tv/recorded/.*|www\.ustream\.tv/channel/.*|www\.ustream\.tv/.*|qik\.com/video/.*|qik\.com/.*|qik\.ly/.*|.*revision3\.com/.*|.*\.dailymotion\.com/video/.*|.*\.dailymotion\.com/.*/video/.*|collegehumor\.com/video:.*|collegehumor\.com/video/.*|www\.collegehumor\.com/video:.*|www\.collegehumor\.com/video/.*|.*twitvid\.com/.*|www\.break\.com/.*/.*|vids\.myspace\.com/index\.cfm\?fuseaction=vids\.individual&videoid.*|www\.myspace\.com/index\.cfm\?fuseaction=.*&videoid.*|www\.metacafe\.com/watch/.*|www\.metacafe\.com/w/.*|blip\.tv/.*/.*|.*\.blip\.tv/.*/.*|video\.google\.com/videoplay\?.*|.*revver\.com/video/.*|video\.yahoo\.com/watch/.*/.*|video\.yahoo\.com/network/.*|sports\.yahoo\.com/video/.*|.*viddler\.com/explore/.*/videos/.*|liveleak\.com/view\?.*|www\.liveleak\.com/view\?.*|animoto\.com/play/.*|dotsub\.com/view/.*|www\.overstream\.net/view\.php\?oid=.*|www\.livestream\.com/.*|www\.worldstarhiphop\.com/videos/video.*\.php\?v=.*|worldstarhiphop\.com/videos/video.*\.php\?v=.*|teachertube\.com/viewVideo\.php.*|www\.teachertube\.com/viewVideo\.php.*|www1\.teachertube\.com/viewVideo\.php.*|www2\.teachertube\.com/viewVideo\.php.*|bambuser\.com/v/.*|bambuser\.com/channel/.*|bambuser\.com/channel/.*/broadcast/.*|www\.schooltube\.com/video/.*/.*|bigthink\.com/ideas/.*|bigthink\.com/series/.*|sendables\.jibjab\.com/view/.*|sendables\.jibjab\.com/originals/.*|www\.xtranormal\.com/watch/.*|socialcam\.com/v/.*|www\.socialcam\.com/v/.*|dipdive\.com/media/.*|dipdive\.com/member/.*/media/.*|dipdive\.com/v/.*|.*\.dipdive\.com/media/.*|.*\.dipdive\.com/v/.*|v\.youku\.com/v_show/.*\.html|v\.youku\.com/v_playlist/.*\.html|www\.snotr\.com/video/.*|snotr\.com/video/.*|video\.jardenberg\.se/.*|www\.clipfish\.de/.*/.*/video/.*|www\.myvideo\.de/watch/.*|www\.whitehouse\.gov/photos-and-video/video/.*|www\.whitehouse\.gov/video/.*|wh\.gov/photos-and-video/video/.*|wh\.gov/video/.*|www\.hulu\.com/watch.*|www\.hulu\.com/w/.*|www\.hulu\.com/embed/.*|hulu\.com/watch.*|hulu\.com/w/.*|.*crackle\.com/c/.*|www\.fancast\.com/.*/videos|www\.funnyordie\.com/videos/.*|www\.funnyordie\.com/m/.*|funnyordie\.com/videos/.*|funnyordie\.com/m/.*|www\.vimeo\.com/groups/.*/videos/.*|www\.vimeo\.com/.*|vimeo\.com/groups/.*/videos/.*|vimeo\.com/.*|vimeo\.com/m/#/.*|www\.ted\.com/talks/.*\.html.*|www\.ted\.com/talks/lang/.*/.*\.html.*|www\.ted\.com/index\.php/talks/.*\.html.*|www\.ted\.com/index\.php/talks/lang/.*/.*\.html.*|.*nfb\.ca/film/.*|www\.thedailyshow\.com/watch/.*|www\.thedailyshow\.com/full-episodes/.*|www\.thedailyshow\.com/collection/.*/.*/.*|movies\.yahoo\.com/movie/.*/video/.*|movies\.yahoo\.com/movie/.*/trailer|movies\.yahoo\.com/movie/.*/video|www\.colbertnation\.com/the-colbert-report-collections/.*|www\.colbertnation\.com/full-episodes/.*|www\.colbertnation\.com/the-colbert-report-videos/.*|www\.comedycentral\.com/videos/index\.jhtml\?.*|www\.theonion\.com/video/.*|theonion\.com/video/.*|wordpress\.tv/.*/.*/.*/.*/|www\.traileraddict\.com/trailer/.*|www\.traileraddict\.com/clip/.*|www\.traileraddict\.com/poster/.*|www\.escapistmagazine\.com/videos/.*|www\.trailerspy\.com/trailer/.*/.*|www\.trailerspy\.com/trailer/.*|www\.trailerspy\.com/view_video\.php.*|www\.atom\.com/.*/.*/|fora\.tv/.*/.*/.*/.*|www\.spike\.com/video/.*|www\.gametrailers\.com/video/.*|gametrailers\.com/video/.*|www\.koldcast\.tv/video/.*|www\.koldcast\.tv/#video:.*|techcrunch\.tv/watch.*|techcrunch\.tv/.*/watch.*|techcrunch\.tv/show/.*/.*|mixergy\.com/.*|video\.pbs\.org/video/.*|www\.zapiks\.com/.*|tv\.digg\.com/diggnation/.*|tv\.digg\.com/diggreel/.*|tv\.digg\.com/diggdialogg/.*|www\.trutv\.com/video/.*|www\.nzonscreen\.com/title/.*|nzonscreen\.com/title/.*|app\.wistia\.com/embed/medias/.*|hungrynation\.tv/.*/episode/.*|www\.hungrynation\.tv/.*/episode/.*|hungrynation\.tv/episode/.*|www\.hungrynation\.tv/episode/.*|indymogul\.com/.*/episode/.*|www\.indymogul\.com/.*/episode/.*|indymogul\.com/episode/.*|www\.indymogul\.com/episode/.*|channelfrederator\.com/.*/episode/.*|www\.channelfrederator\.com/.*/episode/.*|channelfrederator\.com/episode/.*|www\.channelfrederator\.com/episode/.*|tmiweekly\.com/.*/episode/.*|www\.tmiweekly\.com/.*/episode/.*|tmiweekly\.com/episode/.*|www\.tmiweekly\.com/episode/.*|99dollarmusicvideos\.com/.*/episode/.*|www\.99dollarmusicvideos\.com/.*/episode/.*|99dollarmusicvideos\.com/episode/.*|www\.99dollarmusicvideos\.com/episode/.*|ultrakawaii\.com/.*/episode/.*|www\.ultrakawaii\.com/.*/episode/.*|ultrakawaii\.com/episode/.*|www\.ultrakawaii\.com/episode/.*|barelypolitical\.com/.*/episode/.*|www\.barelypolitical\.com/.*/episode/.*|barelypolitical\.com/episode/.*|www\.barelypolitical\.com/episode/.*|barelydigital\.com/.*/episode/.*|www\.barelydigital\.com/.*/episode/.*|barelydigital\.com/episode/.*|www\.barelydigital\.com/episode/.*|threadbanger\.com/.*/episode/.*|www\.threadbanger\.com/.*/episode/.*|threadbanger\.com/episode/.*|www\.threadbanger\.com/episode/.*|vodcars\.com/.*/episode/.*|www\.vodcars\.com/.*/episode/.*|vodcars\.com/episode/.*|www\.vodcars\.com/episode/.*|confreaks\.net/videos/.*|www\.confreaks\.net/videos/.*|video\.allthingsd\.com/video/.*|videos\.nymag\.com/.*|aniboom\.com/animation-video/.*|www\.aniboom\.com/animation-video/.*|clipshack\.com/Clip\.aspx\?.*|www\.clipshack\.com/Clip\.aspx\?.*|grindtv\.com/.*/video/.*|www\.grindtv\.com/.*/video/.*|ifood\.tv/recipe/.*|ifood\.tv/video/.*|ifood\.tv/channel/user/.*|www\.ifood\.tv/recipe/.*|www\.ifood\.tv/video/.*|www\.ifood\.tv/channel/user/.*|logotv\.com/video/.*|www\.logotv\.com/video/.*|lonelyplanet\.com/Clip\.aspx\?.*|www\.lonelyplanet\.com/Clip\.aspx\?.*|streetfire\.net/video/.*\.htm.*|www\.streetfire\.net/video/.*\.htm.*|trooptube\.tv/videos/.*|www\.trooptube\.tv/videos/.*|sciencestage\.com/v/.*\.html|sciencestage\.com/a/.*\.html|www\.sciencestage\.com/v/.*\.html|www\.sciencestage\.com/a/.*\.html|link\.brightcove\.com/services/player/bcpid.*|wirewax\.com/.*|www\.wirewax\.com/.*|canalplus\.fr/.*|www\.canalplus\.fr/.*|www\.vevo\.com/watch/.*|www\.vevo\.com/video/.*|pixorial\.com/watch/.*|www\.pixorial\.com/watch/.*|www\.godtube\.com/featured/video/.*|godtube\.com/featured/video/.*|www\.godtube\.com/watch/.*|godtube\.com/watch/.*|www\.tangle\.com/view_video.*|mediamatters\.org/mmtv/.*|www\.clikthrough\.com/theater/video/.*|espn\.go\.com/video/clip.*|espn\.go\.com/.*/story.*|abcnews\.com/.*/video/.*|abcnews\.com/video/playerIndex.*|abcnews\.go\.com/.*/video/.*|abcnews\.go\.com/video/playerIndex.*|washingtonpost\.com/wp-dyn/.*/video/.*/.*/.*/.*|www\.washingtonpost\.com/wp-dyn/.*/video/.*/.*/.*/.*|www\.boston\.com/video.*|boston\.com/video.*|www\.boston\.com/.*video.*|boston\.com/.*video.*|www\.facebook\.com/photo\.php.*|www\.facebook\.com/video/video\.php.*|www\.facebook\.com/v/.*|cnbc\.com/id/.*\?.*video.*|www\.cnbc\.com/id/.*\?.*video.*|cnbc\.com/id/.*/play/1/video/.*|www\.cnbc\.com/id/.*/play/1/video/.*|cbsnews\.com/video/watch/.*|www\.google\.com/buzz/.*/.*/.*|www\.google\.com/buzz/.*|www\.google\.com/profiles/.*|google\.com/buzz/.*/.*/.*|google\.com/buzz/.*|google\.com/profiles/.*|www\.cnn\.com/video/.*|edition\.cnn\.com/video/.*|money\.cnn\.com/video/.*|today\.msnbc\.msn\.com/id/.*/vp/.*|www\.msnbc\.msn\.com/id/.*/vp/.*|www\.msnbc\.msn\.com/id/.*/ns/.*|today\.msnbc\.msn\.com/id/.*/ns/.*|www\.globalpost\.com/video/.*|www\.globalpost\.com/dispatch/.*|guardian\.co\.uk/.*/video/.*/.*/.*/.*|www\.guardian\.co\.uk/.*/video/.*/.*/.*/.*|bravotv\.com/.*/.*/videos/.*|www\.bravotv\.com/.*/.*/videos/.*|video\.nationalgeographic\.com/.*/.*/.*\.html|dsc\.discovery\.com/videos/.*|animal\.discovery\.com/videos/.*|health\.discovery\.com/videos/.*|investigation\.discovery\.com/videos/.*|military\.discovery\.com/videos/.*|planetgreen\.discovery\.com/videos/.*|science\.discovery\.com/videos/.*|tlc\.discovery\.com/videos/.*|video\.forbes\.com/fvn/.*))|(https://(twitter\.com/.*/status/.*/photo/.*|twitter\.com/.*/statuses/.*/photo/.*|www\.twitter\.com/.*/status/.*/photo/.*|www\.twitter\.com/.*/statuses/.*/photo/.*|mobile\.twitter\.com/.*/status/.*/photo/.*|mobile\.twitter\.com/.*/statuses/.*/photo/.*|skitch\.com/.*/.*/.*|img\.skitch\.com/.*|itunes\.apple\.com/.*|twitter\.com/.*/status/.*|twitter\.com/.*/statuses/.*|www\.twitter\.com/.*/status/.*|www\.twitter\.com/.*/statuses/.*|mobile\.twitter\.com/.*/status/.*|mobile\.twitter\.com/.*/statuses/.*|foursquare\.com/.*|www\.foursquare\.com/.*|crocodoc\.com/.*|.*\.crocodoc\.com/.*|urtak\.com/u/.*|urtak\.com/clr/.*|ganxy\.com/.*|www\.ganxy\.com/.*|.*youtube\.com/watch.*|.*\.youtube\.com/v/.*|app\.wistia\.com/embed/medias/.*|www\.facebook\.com/photo\.php.*|www\.facebook\.com/video/video\.php.*|www\.facebook\.com/v/.*)))'
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
        urlSchemes = ['regex:.*.wordpress\.com/.*',]
        super(WordpressEndPoint, self).__init__(url, urlSchemes=urlSchemes)

    def request(self, url, **opt):
        query = opt
        query['for'] = 'plone'
        return super(WordpressEndPoint, self).request(url, **query)

def load_all_endpoints(embedly_apikey=None):
    endpoints = []
    if embedly_apikey is not None:
        endpoint = EmbedlyEndPoint(embedly_apikey)
        endpoints.append(endpoint)

    endpoint = WordpressEndPoint()
    endpoints.append(endpoint)

    providers = REGEX_PROVIDERS

    for provider in providers:
        endpoint = oembed.OEmbedEndpoint(provider[u'endpoint'],
                                         provider[u'regex'])
        endpoints.append(endpoint)
    
    return endpoints
