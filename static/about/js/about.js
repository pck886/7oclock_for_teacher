$(window).load(function(){

    $('a[href="#credits"]').click(function(event){
        event.preventDefault();
        var target = $(this).attr('href');
        $(target).toggleClass('hidden show');
    });

    $('#btn_send_submit').click('submit', function(e){
        if(e.isDefaultPrevented()) {

            return;
        } else {
            alert("캠페인 신청이 완료되었습니다.");
            return;
        }
    });

    $('#address').click(function(){
        //$('div.modal').modal();
    });
});