/**
 * ブロックコメント判定正規表現
 */
var COMMENT_BLOCK_OPNE_RE = /^{##\s*$/;
var COMMENT_BLOCK_CLOSE_RE = /^(.+\s+|\s*)##}$/;
var COMMENT_INLINE_RE = /^{## .* ##}/;

/**
 * ブロックコメントルール
 */
var block_comment_rule;
block_comment_rule = function (state, startLine, endLine, silent) {
    var ch, match, nextLine, token,
        pos = state.bMarks[startLine],
        max = state.eMarks[startLine];
    pos += state.tShift[startLine];

    if (pos + 2 >= max) {
        return false;
    }

    ch = state.src.charCodeAt(pos);

    // Probably start
    if (ch === 0x7B/* { */) {
        // opening tag
        match = state.src.slice(pos, max).match(COMMENT_BLOCK_OPNE_RE);
        if (!match) {
            return false;
        }
    } else {
        return false;
    }
    // silentがよく分かってません；；
    // おそらくvalidation modeでの動作だと思われる
    if (silent) {
        return true;
    }

    // search a end tag
    nextLine = startLine;
    while (nextLine < state.lineMax) {
        nextLine++;
        pos = state.bMarks[nextLine],
            max = state.eMarks[nextLine];
        if (pos + state.tShift[nextLine] + 2 <= max) {
            if (state.src.slice(pos, max).match(COMMENT_BLOCK_CLOSE_RE)) {
                nextLine++;
                break;
            }
        }
    }

    state.line = nextLine;
    token = state.push('comment_block', '', 0);
    token.map = [startLine, state.line];
    token.content = state.getLines(startLine, nextLine, 0, true);

    return true;
};

/**
 * インラインコメントルール
 */
var inline_comment_rule;
inline_comment_rule = function (state, silent) {
    var ch, code, match, pos = state.pos, max = state.posMax;

    if (state.src.charCodeAt(pos) !== 0x7B/* { */) {
        return false;
    }

    if (pos + 1 < max) {
        ch = state.src.charCodeAt(pos + 1);

        if (ch === 0x23 /* # */) {
            match = state.src.slice(pos).match(COMMENT_INLINE_RE);
            if (match) {
                state.pos += match[0].length;
                return true;
            }
        }
    }
    return false;
};

/**
 * コメントレンダリングルール
 */
var comment_render_rule;
comment_render_rule = function (tokens, idx, options, env, self) {
    return '';
};


// Because highlight.js is a bit awkward at times
var languageOverrides = {
    js: 'javascript',
    html: 'xml'
};

var markdownRender = function () {
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
            , linkify: true
        }).use(markdownitFootnote); //注釈機能の追加:https://www.npmjs.com/package/markdown-it-footnote

    //コメントルールの追加
    md.block.ruler.after('fence', 'comment_block', block_comment_rule);
    md.inline.ruler.after('image', 'comment_block', inline_comment_rule);
    md.renderer.rules.comment_block = comment_render_rule;

    markdownRender.prototype.render = function (val) {
        if (!md) {
            return "";
        }
        val = val.replace(/<equation>((.*?\n)*?.*?)<\/equation>/ig, function (a, b) {
            var equation = encodeURIComponent(b);
            return '![' + equation + '](http://latex.codecogs.com/png.latex?' + equation + ")";
        }); //LaTeX変換
        return md.render(val);
    };
};

