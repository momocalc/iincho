/**
 * ユニーク文字列の取得
 * 厳密なユニーク文字列が必要ならUUIDなどを利用すること．
 * @param myStrong
 * @returns {string}
 */
function getUniqueStr(myStrong) {
    var strong = 1000;
    if (myStrong) strong = myStrong;
    return new Date().getTime().toString(16) + Math.floor(strong * Math.random()).toString(16)
}
