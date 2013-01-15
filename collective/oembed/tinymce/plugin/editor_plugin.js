/**
 * Plone collective.oembed plugin.
 * 
 * @author JeanMichel FRANCOIS aka toutpt
 */

(function() {
	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('oembed');
	var each = tinymce.each;

	tinymce.create('tinymce.plugins.Oembed', {
		init : function(ed, url) {
			tinymce.DOM.loadCSS(url + '/css/editor.css');
			// Register commands
			ed.addCommand('mceOembed', function(ui) {
				ed.windowManager.open({
					file : url + '/oembed.htm',
					width : 320 + parseInt(ed.getLang('oembed.delta_width', 0)),
					height: 120 + parseInt(ed.getLang('oembed.delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.addCommand('mceOembedInsert', t._insertOembed, t);

			// Register buttons
			ed.addButton('oembed', {
				title : 'oembed.desc',
				cmd : 'mceOembedDialog',
				image : url + '/img/oembed.gif'
			});

			ed.onPreProcess.add(function(ed, o) {
				var dom = ed.dom;

				each(dom.select('div', o.node), function(e) {
					console.log('??');
				});
			});
		},

		getInfo : function() {
			return {
				longname : 'OEmbed pluin',
				author : 'JeanMichel FRANCOIS aka toutpt',
				authorurl : 'http://www.makina-corpus.com',
				infourl : 'https://github.com/collective.oembed',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		},

		_insertOembed : function(ui, v) {
			console.log('insert');
			var t = this, ed = t.editor, h, el, dom = ed.dom, sel = ed.selection.getContent();

			h = v.content;

			el = dom.create('a', null, h);

			ed.execCommand('mceInsertContent', false, el.innerHTML);
			ed.addVisual();
		},

	});

	// Register plugin
	console.log('register plugin');
	tinymce.PluginManager.add('collectiveoembed', tinymce.plugins.Oembed);
})();