/**
 * Plone collective.oembed plugin.
 *
 * @author JeanMichel FRANCOIS aka toutpt
 */

(function() {
    var each = tinymce.each;

    tinymce.create('tinymce.plugins.CollectiveOembed', {
        init : function(ed, url) {
            var t = this;

            t.editor = ed;

            // Register css
            //tinymce.DOM.loadCSS(url + '/css/content.css');

            // Register commands
            ed.addCommand('mceCollectiveOembedDialog', function(ui) {
                ed.windowManager.open({
                    file : url + '/oembed.htm',
                    width : ed.getParam('template_popup_width', 750),
                    height : ed.getParam('template_popup_height', 600),
                    inline : 1
                }, {
                    plugin_url : url
                });
            });

            ed.addCommand('mceCollectiveOembedInsert', t._insertOembed, t);

            // Register buttons
            ed.addButton('collectiveoembed', {title : 'collectiveoembed.desc', cmd : 'mceCollectiveOembedDialog'});

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
    tinymce.PluginManager.add('collectiveoembed', tinymce.plugins.CollectiveOembed);
})();