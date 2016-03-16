/*
 * 引数のオブジェクトを非活性に設定する
 */
function setDisable(control){
    setTimeout(function(){
      control.disabled=true;
    },1);
}
