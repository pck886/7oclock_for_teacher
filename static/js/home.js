$(window).load(function(){
    var day = ["일","월","화","수","목","금","토"];
    var myDate = new Date();
    $("#p_top_date").text(myDate.getFullYear()+"년 "+(myDate.getMonth()+1)+"월 "+myDate.getDate()+"일 "+day[myDate.getDay()%7]+"요일");

    $('#JoinModal #uid').keyup(function(){
        if($(this).val().length < 4){
            setChk("btn_join_chkid",false, "아이디가 너무 짧습니다.");
        }else{
            $.ajax({type:"POST", url:"/user/join/get/", data:{'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),'userid':$("#JoinModal #uid").val()},
                success:function(args){
                    if(args == 1){
                        setChk("btn_join_chkid",true, "사용가능한 아이디입니다.");
                    }else{
                        setChk("btn_join_chkid",false, "이미 가입된 아이디입니다.");
                    }
                }
            });
        }
    });

    $('#JoinModal #upw').keyup(function(){
        if($(this).val().length < 6){
            setChk("btn_join_chkpw",false, "6자리 이상을 입력하세요.");
        }else{
            setChk("btn_join_chkpw",true, "사용가능한 비밀번호입니다.");
        }
    });

    $('#JoinModal #upw_').keyup(function(){
        if($(this).val() != $('#JoinModal #upw').val()){
            setChk("btn_join_chkpw_",false, "위 비밀번호와 똑같이 입력하세요.");
        }else{
            setChk("btn_join_chkpw_",true, "사용가능한 비밀번호입니다.");
        }
    });

    $('#JoinModal #uemail').keyup(function(){
        if(!validateEmail($(this).val())){
            setChk("btn_join_chkemail",false, "잘못된 이메일 형식입니다.");
        }else{
            $.ajax({type:"POST", url:"/user/join/get/", data:{'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),'email':$("#JoinModal #uemail").val()},
                success:function(args){
                    if(args == 1){
                        setChk("btn_join_chkemail",true, "사용 가능한 이메일입니다.");
                    }else{
                        setChk("btn_join_chkemail",false, "이미 가입된 이메일입니다.");
                    }
                }
            });
        }
    });

    $("#JoinModal #btn_join_submit").click(function(){
        var chk_id = Number($("#JoinModal  #btn_join_chkid").attr("chk"));
        var chk_pw = Number($("#JoinModal  #btn_join_chkpw").attr("chk"));
        var chk_pw_ = Number($("#JoinModal  #btn_join_chkpw_").attr("chk"));
        var chk_name = Number($("#JoinModal  #uname").val().length);
        var chk_email = Number($("#JoinModal  #btn_join_chkemail").attr("chk"));
        var chk_phone = Number($("#JoinModal  #uphone").val().length);
        var chk_opt = Number($(":checkbox[id='check_opt']:checked").length);

        if(chk_id == 0){
            $("#JoinModal  #uid").focus();
            return;
        }else if(chk_pw == 0){
            $("#JoinModal  #upw").focus();
            return;
        }else if(chk_pw_ == 0){
            $("#JoinModal  #upw_").focus();
            return;
        }else if(chk_name == 0){
            $("#JoinModal  #uname").focus();
            return;
        }else if(chk_email == 0){
            $("#JoinModal  #uemail").focus();
            return;
        }else if(chk_phone == 0){
            $("#JoinModal  #uphone").focus();
            return;
        }else if(chk_opt == 0){
            $("#JoinModal  #check_opt").focus();
            return;
        }

        $("#JoinModal #form_join").submit();
    });

    $('#JoinModal #uschool').focus(function(evt){
        if($("#uschool").val() != "") getSearchList($('#JoinModal #uschool').val());
    });

    $('#JoinModal #uschool').change(function(evt){
        getSearchList($('#JoinModal #uschool').val());
    });

    $('#JoinModal #uschool').keyup(function(evt){
        getSearchList($('#JoinModal #uschool').val());
    });

});

function getSearchList(q){
    $('.div_list_school').show();
    $('.div_list_school').load('/home/list/school/',{
        'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
        'q':q
    });
}

function setChk(ele_id, chk, msg){
    if(chk){
        $("#"+ele_id).html('<i class="xi-check-circle success"></i>');
        $("#"+ele_id).attr({'title':msg,'chk':1});
    }else{
        $("#"+ele_id).html('<i class="xi-ban-circle fail"></i>');
        $("#"+ele_id).attr({'title':msg,'chk':0});
    }
}

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}