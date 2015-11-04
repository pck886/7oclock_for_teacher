$(window).load(function(){

    redirect();

    $("#p_wrap_company").click(function(){
        link("/");
    });

});

function redirect(){
    var str_url = window.location.href;

    if((str_url.indexOf("mathforall") < 0)||(str_url.indexOf("www") < 0)) window.location.href = "http://www.mathforall.net/";
}

function link(src){
    if(src=='back') history.go(-1);
    else location.href = src;
}