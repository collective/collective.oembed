/*!
 * jquery oembed plugin modified to use
 * plone as main provider
 *
 * Copyright (c) 2009 Richard Chamorro
 * Licensed under the MIT license
 * 
 * Author: Richard Chamorro 
 * Contributor: JeanMichel FRANCOIS
 * 
 * Modifications: remove callback param (no more JSONP) to use Plone
 * as only provider
 */

(function ($) {
	$.fn.oembed = function (url, options, embedAction) {

		settings = $.extend(true, $.fn.oembed.defaults, options);

		initializeProviders();

		var div = document.createElement('div'),
		ref = document.getElementsByTagName('base')[0] || document.getElementsByTagName('script')[0];

		div.className = 'fit-vids-style';
		div.innerHTML = '&shy;<style>     \
      .fluid-width-video-wrapper {        \
         width: 100%;                     \
         position: relative;              \
         padding: 0;                      \
      }                                   \
                                          \
      .fluid-width-video-wrapper iframe,  \
      .fluid-width-video-wrapper object,  \
      .fluid-width-video-wrapper embed {  \
         position: absolute;              \
         top: 0;                          \
         left: 0;                         \
         width: 100%;                     \
         height: 100%;                    \
      }                                   \
    </style>';

		ref.parentNode.insertBefore(div,ref);

		return this.each(function () {
			var container = $(this),
			resourceURL = (url != null) ? url : container.attr("href"), provider;

			if (embedAction) {
				settings.onEmbed = embedAction;
			} else {
				settings.onEmbed = function (oembedData) {
					$.fn.oembed.insertCode(this, settings.embedMethod, oembedData);
				};
			}

			if (resourceURL != null) {
				provider = $.fn.oembed.getOEmbedProvider(resourceURL);

				if (provider != null) {
					provider.params = getNormalizedParams(settings[provider.name]) || {};
					provider.maxWidth = settings.maxWidth;
					provider.maxHeight = settings.maxHeight;
					embedCode(container, resourceURL, provider);
				} else {
					settings.onProviderNotFound.call(container, resourceURL);
				}
			}

			return container;
		});


	};

	var settings, activeProviders = [];

	// Plugin defaults
	$.fn.oembed.defaults = {
			maxWidth: null,
			maxHeight: null,
			embedMethod: "replace",  	// "auto", "append", "fill"		
			defaultOEmbedProvider: "plone", 	// "oohembed", "embed.ly", "none"
			allowedProviders: null,
			disallowedProviders: null,
			customProviders: null, // [ new $.fn.oembed.OEmbedProvider("customprovider", null, ["customprovider\\.com/watch.+v=[\\w-]+&?"]) ]	
			defaultProvider: null,
			greedy: true,
			onProviderNotFound: function () { },
			beforeEmbed: function () { },
			afterEmbed: function () { },
			onEmbed: function () { },
			onError: function() {},
			ajaxOptions: {}
	};

	/* Private functions */
	function getRequestUrl(container, externalUrl, provider) {

		var url = provider.apiendpoint, qs = ""
//			var callbackparameter = provider.callbackparameter || "callback", 
			var i;

		if (url.indexOf("?") <= 0)
			url = url + "?";
		else
			url = url + "&";

		if (provider.maxWidth != null && provider.params["maxwidth"] == null)
			provider.params["maxwidth"] = provider.maxWidth;
		if (provider.maxHeight != null && provider.params["maxheight"] == null)
			provider.params["maxheight"] = provider.maxHeight;

		for (i in provider.params) {
			// allows the options to be set to null, don't send null values to the server as parameters
			if (provider.params[i] != null)
				qs += "&" + escape(i) + "=" + provider.params[i];
		}

		url += "format=json&url=" + escape(externalUrl) +
			qs ;

		if (container[0].dataset.maxwidth != undefined)
			url += "&maxwidth=" + container[0].dataset.maxwidth;
		if (container[0].dataset.maxheight != undefined)
			url += "&maxheight=" + maxcontainer[0].dataset.maxheight;

		return url;
	};

	function embedCode(container, externalUrl, embedProvider) {

		var requestUrl = getRequestUrl(container, externalUrl, embedProvider);
		var ajaxopts = $.extend({
			url: requestUrl,
			type: 'get',
			dataType: 'json',
			// error: jsonp request doesnt' support error handling
			success:  function (data) {
				var oembedData = $.extend({}, data);
				switch (oembedData.type) {
				case "photo":
					oembedData.code = $.fn.oembed.getPhotoCode(externalUrl, oembedData);
					break;
				case "video":
					oembedData.code = $.fn.oembed.getVideoCode(externalUrl, oembedData);
					break;
				case "rich":
					oembedData.code = $.fn.oembed.getRichCode(externalUrl, oembedData);
					break;
				default:
					oembedData.code = $.fn.oembed.getGenericCode(externalUrl, oembedData);
				break;
				}
				settings.beforeEmbed.call(container, oembedData);
				settings.onEmbed.call(container, oembedData);
				settings.afterEmbed.call(container, oembedData);
			},
			error: function (xhr, ajaxOptions, thrownError) {
				console.log(xhr.responseText);
				console.log(thrownError);
			}
			//error: settings.onError.call(container, externalUrl, embedProvider)
		}, settings.ajaxOptions || { } );

		$.ajax( ajaxopts );
	};

	function initializeProviders() {

		activeProviders = [];

		var defaultProvider, restrictedProviders = [], i, provider;

		if (!isNullOrEmpty(settings.allowedProviders)) {
			for (i = 0; i < $.fn.oembed.providers.length; i++) {
				if ($.inArray($.fn.oembed.providers[i].name, settings.allowedProviders) >= 0)
					activeProviders.push($.fn.oembed.providers[i]);
			}
			// If there are allowed providers, jquery-oembed cannot be greedy
			settings.greedy = false;

		} else {
			activeProviders = $.fn.oembed.providers;
		}

		if (!isNullOrEmpty(settings.disallowedProviders)) {
			for (i = 0; i < activeProviders.length; i++) {
				if ($.inArray(activeProviders[i].name, settings.disallowedProviders) < 0)
					restrictedProviders.push(activeProviders[i]);
			}
			activeProviders = restrictedProviders;
			// If there are allowed providers, jquery-oembed cannot be greedy
			settings.greedy = false;
		}

		if (!isNullOrEmpty(settings.customProviders)) {
			$.each(settings.customProviders, function (n, customProvider) {
				if (customProvider instanceof $.fn.oembed.OEmbedProvider) {
					activeProviders.push(provider);
				} else {
					provider = new $.fn.oembed.OEmbedProvider();
					if (provider.fromJSON(customProvider))
						activeProviders.push(provider);
				}
			});
		}

		// If in greedy mode, we add the default provider
		defaultProvider = getDefaultOEmbedProvider(settings.defaultOEmbedProvider);
		if (settings.greedy == true) {
			activeProviders.push(defaultProvider);
		}
		// If any provider has no apiendpoint, we use the default provider endpoint
		for (i = 0; i < activeProviders.length; i++) {
			if (activeProviders[i].apiendpoint == null)
				activeProviders[i].apiendpoint = defaultProvider.apiendpoint;
		}
	}

	function getDefaultOEmbedProvider(defaultOEmbedProvider) {
		var url = "http://oohembed.com/oohembed/";
		if (defaultOEmbedProvider == "embed.ly")
			url = "http://api.embed.ly/v1/api/oembed?";
		if (defaultOEmbedProvider == "plone")
			url = portal_url + '/@@proxy-oembed-provider'
			return new $.fn.oembed.OEmbedProvider(defaultOEmbedProvider, null, null, url, "callback");
	}

	function getNormalizedParams(params) {
		if (params == null)
			return null;
		var key, normalizedParams = {};
		for (key in params) {
			if (key != null)
				normalizedParams[key.toLowerCase()] = params[key];
		}
		return normalizedParams;
	}

	function isNullOrEmpty(object) {
		if (typeof object == "undefined")
			return true;
		if (object == null)
			return true;
		if ($.isArray(object) && object.length == 0)
			return true;
		return false;
	}

	/* Public functions */
	$.fn.oembed.insertCode = function (container, embedMethod, oembedData) {
		if (oembedData == null)
			return;

		switch (embedMethod) {
		case "auto":
			if (container.attr("href") != null) {
				$.fn.oembed.insertCode(container, "append", oembedData);
			}
			else {
				$.fn.oembed.insertCode(container, "replace", oembedData);
			};
			break;
		case "replace":
			if (container.hasClass("oembed-responsive")){
				var html = $(oembedData.code);
		        if (html.is("iframe")){
		            /*make it responsive*/
		            var width = parseInt(html.attr("width")), height = parseInt(html.attr("height"));
		            var ratio = height / width;
		            container.wrap('<div class="fluid-width-video-wrapper"></div>').parent('.fluid-width-video-wrapper').css('padding-top', (ratio * 100)+"%");
		            html.removeAttr('height').removeAttr('width');
		            oembedData.code = html[0].outerHTML;
		        }
			}
			container.replaceWith(oembedData.code);
			break;
		case "fill":
			container.html(oembedData.code);
			break;
		case "append":
			var oembedContainer = container.next();
			if (oembedContainer == null || !oembedContainer.hasClass("oembed-container")) {
				oembedContainer = container
				.after('<div class="oembed-container"></div>')
				.next(".oembed-container");
				if (oembedData != null && oembedData.provider_name != null)
					oembedContainer.toggleClass("oembed-container-" + oembedData.provider_name);
			}
			oembedContainer.html(oembedData.code);
			break;
		}
	};

	$.fn.oembed.getPhotoCode = function (url, oembedData) {
		var code, alt = oembedData.title ? oembedData.title : '';
		alt += oembedData.author_name ? ' - ' + oembedData.author_name : '';
		alt += oembedData.provider_name ? ' - ' + oembedData.provider_name : '';
		code = '<div><a href="' + url + '" target=\'_blank\'><img src="' + oembedData.url + '" alt="' + alt + '"/></a></div>';
		if (oembedData.html)
			code += "<div>" + oembedData.html + "</div>";
		return code;
	};

	$.fn.oembed.getVideoCode = function (url, oembedData) {
		var code = oembedData.html;

		return code;
	};

	$.fn.oembed.getRichCode = function (url, oembedData) {
		var code = oembedData.html;
		return code;
	};

	$.fn.oembed.getGenericCode = function (url, oembedData) {
		var title = (oembedData.title != null) ? oembedData.title : url,
				code = '<a href="' + url + '">' + title + '</a>';
		if (oembedData.html)
			code += "<div>" + oembedData.html + "</div>";
		return code;
	};

	$.fn.oembed.isProviderAvailable = function (url) {
		var provider = getOEmbedProvider(url);
		return (provider != null);
	};

	$.fn.oembed.getOEmbedProvider = function (url) {
		for (var i = 0; i < activeProviders.length; i++) {
			if (activeProviders[i].matches(url))
				return activeProviders[i];
		}
		return null;
	};

	$.fn.oembed.OEmbedProvider = function (name, type, urlschemesarray, apiendpoint, callbackparameter) {
		this.name = name;
		this.type = type; // "photo", "video", "link", "rich", null
		this.urlschemes = getUrlSchemes(urlschemesarray);
		this.apiendpoint = apiendpoint;
		this.callbackparameter = callbackparameter;
		this.maxWidth = 500;
		this.maxHeight = 400;
		var i, property, regExp;

		this.matches = function (externalUrl) {
			for (i = 0; i < this.urlschemes.length; i++) {
				regExp = new RegExp(this.urlschemes[i], "i");
				if (externalUrl.match(regExp) != null)
					return true;
			}
			return false;
		};

		this.fromJSON = function (json) {
			for (property in json) {
				if (property != "urlschemes")
					this[property] = json[property];
				else
					this[property] = getUrlSchemes(json[property]);
			}
			return true;
		};

		function getUrlSchemes(urls) {
			if (isNullOrEmpty(urls))
				return ["."];
			if ($.isArray(urls))
				return urls;
			return urls.split(";");
		}
	};

	/* Native & common providers */
	$.fn.oembed.providers = [];

})(jQuery);