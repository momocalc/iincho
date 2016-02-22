// Because highlight.js is a bit awkward at times
var languageOverrides = {
    js: 'javascript',
    html: 'xml'
};

var markdownRender = function() {
    var md =
        markdownit({
            html: false,
            breaks: true,
            highlight: function (code, lang) {
                if (languageOverrides[lang]) lang = languageOverrides[lang];
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(lang, code).value;
                    } catch (e) {
                    }
                }
                return '';
            }
            ,linkify:true
        }).use(markdownitFootnote); //注釈機能の追加:https://www.npmjs.com/package/markdown-it-footnote

    markdownRender.prototype.render = function(val){
        if (!md){ return ""; }
        val = val.replace(/<equation>((.*?\n)*?.*?)<\/equation>/ig, function(a, b){
            return '<img src="http://latex.codecogs.com/png.latex?' + encodeURIComponent(b) + '" />';
        }); //LaTeX変換
        return md.render(val);
    };
};



