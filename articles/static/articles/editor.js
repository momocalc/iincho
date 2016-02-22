
var URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
navigator.saveBlob = navigator.saveBlob || navigator.msSaveBlob || navigator.mozSaveBlob || navigator.webkitSaveBlob;
window.saveAs = window.saveAs || window.webkitSaveAs || window.mozSaveAs || window.msSaveAs;

$(function(){
    function editor_adjust(){
        var h = $(window).height(); //ウィンドウの高さ
        var h1= $('#top-nav').height() + $('.editor-footer').height(); //他要素の高さ
        h1 = h1 + 80;
        $('.editor-textarea').css('height', h-h1); //可変部分の高さを適用
    }

    editor_adjust();

    $(window).on('resize', function(){
        editor_adjust();
    });

    // title-change-event
    $("#article-title").change(function(){
        $("#title-out").text($(this).val());
    });
    $("#title-out").text($("#article-title").val());

    $("#article-title").focus();
});

var hashto;

function update(e){
    setOutput(e.getValue());

    clearTimeout(hashto);
    hashto = setTimeout(updateHash, 1000);
}

var md = new markdownRender();
function setOutput(val){

    var out = document.getElementById('out');
    var old = out.cloneNode(true);
    out.innerHTML = md.render(val);
    emojify.run(out);

    var allold = old.getElementsByTagName("*");
    if (allold === undefined) return;

    var allnew = out.getElementsByTagName("*");
    if (allnew === undefined) return;

    // 編集箇所にスクロール
    for (var i = 0, max = Math.min(allold.length, allnew.length); i < max; i++) {
        if (!allold[i].isEqualNode(allnew[i])) {
            $(".editor-preview").scrollTop(allnew[i].offsetTop - 50);
            return;
        }
    }
}

var editor = CodeMirror.fromTextArea(document.getElementById('article-code'), {
    mode: 'gfm',
    lineNumbers: false,
    matchBrackets: true,
    lineWrapping: true,
    dragDrop: false,
    theme: 'base16-light',
    extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"}
});

editor.on('change', update);

//key event
document.addEventListener('keydown', function(e){
    if(e.keyCode == 83 && (e.ctrlKey || e.metaKey)){ //cmd + S
        // e.shiftKey ? showMenu() : saveAsMarkdown();

        e.preventDefault();
        return false;
    }
//      if(e.keyCode === 27 && menuVisible){
//        hideMenu();
//
//        e.preventDefault();
//        return false;
//      }
});

function updateHash(){
    window.location.hash = btoa( // base64 so url-safe
        RawDeflate.deflate( // gzip
            unescape(encodeURIComponent( // convert to utf8
                editor.getValue()
            ))
        )
    );
}

if(window.location.hash){
    var h = window.location.hash.replace(/^#/, '');
    if(h.slice(0,5) == 'view:'){
        setOutput(decodeURIComponent(escape(RawDeflate.inflate(atob(h.slice(5))))));
        document.body.className = 'view';
    }else{
        editor.setValue(
            decodeURIComponent(escape(
                RawDeflate.inflate(
                    atob(
                        h
                    )
                )
            ))
        );
        update(editor);
        editor.focus();
    }
}else {
    update(editor);
    editor.focus();
}
