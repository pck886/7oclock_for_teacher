var union_id = 0;
var is_changed = false;
var item_no = 0;
var select_url = '';
var alert_value = {};

$(window).load(function(){
    union_id = $("#div_header_union").attr("union_id");
    link_content({'link':'dashboard'});
    $("#div_header_union_tootip").tooltip('show');
});

$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip();

    $('input[type=radio], input[type=checkbox]').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });

    $("#div_modal_searchunion #btn_searchunion_submit").click(function(){
        var union_id = $("#div_modal_searchunion #union_id").val();

        $.post("/main/dashboard/post/union/register/",{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            'union_id':union_id,
        },function(data){
            location.href="/main/?id="+data;
        });
    });

    $("#div_modal_makeunion #btn_makeunion_submit").click(function(){
        var union_id = $("#div_header_union").attr('union_id');;

        $.post("/main/dashboard/post/group/register/", {
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            'union_id' : union_id,
            'title' : $("#input_makeunion_ele_name").val(),
            'adres' : $("#input_makeunion_ele_adres").val()
        }, function(data, err) {
            if(data == "False") {
                alert("결제가 되지 않았습니다.");
            } else {
                alert("소속 등록이 완료되었습니다.");
            }
            location.reload(true);
            //location.href = "/main/?id="+data;
        });
    });

     $("#div_modal_makeunion #input_makeunion_ele_adres").keyup(function(e){
         var code = e.keyCode || e.which;

         if(code == 9)
            $("#div_modal_makeunion #input_makeunion_ele_adres").click();
     });

    $("#div_modal_makeunion #input_makeunion_ele_adres").click(function(){
        new daum.Postcode({
            oncomplete: function(data) {
                // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

                // 도로명 주소의 노출 규칙에 따라 주소를 조합한다.
                // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
                var fullRoadAddr = data.roadAddress; // 도로명 주소 변수
                var extraRoadAddr = ''; // 도로명 조합형 주소 변수

                // 법정동명이 있을 경우 추가한다. (법정리는 제외)
                // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
                if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
                    extraRoadAddr += data.bname;
                }
                // 건물명이 있고, 공동주택일 경우 추가한다.
                if(data.buildingName !== '' && data.apartment === 'Y'){
                   extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                }
                // 도로명, 지번 조합형 주소가 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
                if(extraRoadAddr !== ''){
                    extraRoadAddr = ' (' + extraRoadAddr + ')';
                }
                // 도로명, 지번 주소의 유무에 따라 해당 조합형 주소를 추가한다.
                if(fullRoadAddr !== ''){
                    fullRoadAddr += extraRoadAddr;
                }

                // 우편번호와 주소 정보를 해당 필드에 넣는다.
                //document.getElementById('sample4_postcode').value = data.zonecode; //5자리 새우편번호 사용
                document.getElementById('input_makeunion_ele_adres').value = fullRoadAddr;
                //document.getElementById('sample4_jibunAddress').value = data.jibunAddress;

                // 사용자가 '선택 안함'을 클릭한 경우, 예상 주소라는 표시를 해준다.
                if(data.autoRoadAddress) {
                    //예상되는 도로명 주소에 조합형 주소를 추가한다.
                    var expRoadAddr = data.autoRoadAddress + extraRoadAddr;
                    document.getElementById('guide').innerHTML = '(예상 도로명 주소 : ' + expRoadAddr + ')';

                } else if(data.autoJibunAddress) {
                    var expJibunAddr = data.autoJibunAddress;
                    document.getElementById('guide').innerHTML = '(예상 지번 주소 : ' + expJibunAddr + ')';

                } else {
                    document.getElementById('guide').innerHTML = '';
                }
            }
        }).open();
    });

    $("#wrap #container #div_main_dark").click(function(){
        $("#wrap #container #div_main_dark").hide();
        $('#div_header_union').css({"z-index":"initial"});
    });

    function getSearchSchoolList(q, grade){
        $('.div_list_school').show();
        $('.div_list_school').load('/home/list/school/',{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            'q':q, 'grade':grade
        });
    }

    $('#div_modal_welcome2 #input_dashboard_ele2_school').focus(function(evt){
        if($("#input_dashboard_ele2_school").val() != "") getSearchSchoolList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
    });

    $('#div_modal_welcome2 #input_dashboard_ele2_school').change(function(evt){
        if($("#input_dashboard_ele2_school").val() != "") getSearchSchoolList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
        else $('.div_list_school').hide();
    });

    $('#div_modal_welcome2 #input_dashboard_ele2_school').keyup(function(evt){
        getSearchSchoolList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
    });

    function getSearchUnionList(q){
        $('.div_list_union').show();
        $('.div_list_union').load('/home/list/union/',{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            'q':q
        });
    }

    $('#div_modal_searchunion #input_searchunion_ele_name').focus(function(evt){
        if($("#input_searchunion_ele_name").val() != "") getSearchUnionList($('#div_modal_searchunion #input_searchunion_ele_name').val());
    });

    $('#div_modal_searchunion #input_searchunion_ele_name').change(function(evt){
        if($("#input_searchunion_ele_name").val() != "") getSearchUnionList($('#div_modal_searchunion #input_searchunion_ele_name').val());
        else $('.div_list_school').hide();
    });

    $('#div_modal_searchunion #input_searchunion_ele_name').keyup(function(evt){
        getSearchUnionList($('#div_modal_searchunion #input_searchunion_ele_name').val());
    });

    $("#input_maketest_title").keyup(function(){
        var str = $(this).val();
        $.post("/select/post/maketest/chkname/",{'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),'keyword':str},function(data){
            $('#btn_maketest_submit').attr('disabled','disabled');
            if(data == 0){
                $("#span_maketest_chkname i").hide();
                $("#span_maketest_chkname i.success").show();
                $('#btn_maketest_submit').removeAttr('disabled');
                return;
            }
            $("#span_maketest_chkname i").hide();
            $("#span_maketest_chkname i.fail").show();
        });
    });

    $("#btn_maketest_submit").click(function(){
        var input_maketest_tpid= $("#div_modal_maketest #input_maketest_tpid").val();
        var input_maketest_title = $("#div_modal_maketest #input_maketest_title").val();
        var radio_inventory_purpose = $("#div_modal_maketest input[name=maketest_purpose]:checked").val();
        var questions = "";
        var arr = {};

        if(input_maketest_tpid){
            $("#div_main_loading").show();
            select_url = "/select/post/maketest/";
            arr = {
                'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
                'union_id':union_id,
                'title':input_maketest_title,
                'tpid':input_maketest_tpid,
                'purpose':radio_inventory_purpose
            };
        }else{
            $("#div_select_box #div_box_contents .list").each(function(i){
                questions += $(this).attr('question_id')+",";
            });
            questions = questions.substring(0,questions.length-1);

            $("#div_main_loading").show();
            select_url = "/select/post/maketest/";
            arr = {
                'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
                'union_id':union_id,
                'title':input_maketest_title,
                'questions':questions,
                'purpose':radio_inventory_purpose
            };
        }

        $("#content").load(select_url,arr,function(){
            $("#div_modal_maketest #input_maketest_tpid").val('');
            $("#div_modal_maketest #input_maketest_title").val('');
            $("#span_maketest_chkname i").hide();
            $("#span_maketest_chkname i.default").show();
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, "div_testpaper_answer"]);
            $("#div_main_loading").fadeOut();
        });
        $("#wrap #container #div_select_box").hide();
        $("#div_modal_maketest").modal('hide');
        is_changed = false;
    });

    $("#btn_alert_submit").click(function(){
        $(alert_value.load_id).load(alert_value.url,alert_value.data,alert_value.function);
        alert_value = {};
        $("#div_modal_alert").modal("hide");
    });

    //$("#div_modal_mypage_ele1 #btn_mypage_ele_submit").click(function(){
    //    $.post("/main/mypage/post/group/change/",{
    //        'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
    //        'sid':$('#div_modal_mypage_ele1 #uGroupid').val()
    //    },function(data){
    //        location.reload(true);
    //    });
    //});
    //
    //$('#div_modal_mypage_ele1 #input_mypage_ele1_change').focus(function(evt){
    //    if($("#input_mypage_ele1_now").val() != "") getSearchSchoolList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});
    //
    //$('#div_modal_mypage_ele1 #input_mypage_ele1_change').change(function(evt){
    //    getSearchSchoolList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});
    //
    //$('#div_modal_mypage_ele1 #input_mypage_ele1_change').keyup(function(evt){
    //    getSearchSchoolList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});



});

function search_union(){
    $("#wrap #container #div_main_dark").hide();
    $('#div_header_union').css({"z-index":"initial"});
    $("#div_modal_searchunion").modal("show");
}

function make_union(){
    $("#wrap #container #div_main_dark").hide();
    $('#div_header_union').css({"z-index":"initial"});
    $("#div_modal_makeunion").modal("show");
}

function setting_union(){
    $("#wrap #container #div_main_dark").hide();
    $('#div_header_union').css({"z-index":"initial"});
    $("#div_modal_setunion").modal("show");
}

function link_dashboard_union(){
    $("#div_main_loading").show();
    $(".div_content_board_dashboard #div_dashboard_board").load("/dashboard/union/",{
        'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        ,'union_id':union_id
    },function(data, err){
        $("#div_main_loading").fadeOut();
        //if(err == "error") location.reload(true);
    });
    $("#wrap #container #div_select_box").hide();
}

function alert_show(arr){
    alert_value = arr;
    $("#div_modal_alert .p_page_title").html(alert_value.title);
    $("#div_modal_alert .div_page_contents").html(alert_value.contents);
    $("#div_modal_alert").modal("show");
}

function del_search(){
    $("#input_search_bar").val("");
    set_search();
}

function link_content(obj){

    var request_msg = "";

    if(is_changed){
        var r = confirm("내용이 변경되었습니다. 이 페이지에서 벗어나시겠습니까?");
        if (r != true){
            return;
        }
        is_changed = false;
    }

    $("#div_main_loading").show();

    if(obj.link == 'home') {
        select_url = "/main/?id="+union_id;
        location.href=select_url;
    }else if(obj.link == 'dashboard'){
        select_url = "/dashboard/";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            link_dashboard_union();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'inventory'){
        select_url = "/inventory/";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'select'){
        select_url = "/select/?unit1=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").show();
        $("#wrap #container #div_select_box #div_box_contents").html("")
    }else if(obj.link == 'testpaper'){
        select_url = "/testpaper/?tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            // if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'testpaper_modify'){
        select_url = "/testpaper/modify/?unit1=0&tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").show();
        $("#wrap #container #div_select_box #div_box_contents").html("")
    }else if(obj.link == 'testpaper_form'){
        select_url = "/testpaper/form/?tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'testpaper_similar'){
        select_url = "/testpaper/similar/?tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'progress'){
        select_url = "/progress/?year=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'mypage'){
        select_url = "/mypage/?";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'groupuser'){
        select_url = "/groupuser/?id="+obj.group_id;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        },function(data, err){
            $("#div_main_loading").fadeOut();
            //if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'payment'){
        select_url = "/payment/?id=" + obj.group_id;
        $.post(select_url, {
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
            ,'union_id':union_id
        }, function(data, err){
            if(data == 'True') {
                alert("무료 신청이 완료 되었습니다.");
            } else if(data == 'False'){
                alert("이미 무료 신청이 완료 되었습니다.");
            }

            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
    }

}

function get_or_0(v){
    if(v) return v;
    return 0;
}

window.onbeforeunload = function() {
    if(is_changed){
        return '내용이 변경되었습니다. 이 페이지에서 벗어나시겠습니까?';
    }
}

window.onload = function () {
    if (typeof history.pushState === "function") {
        history.pushState("jibberish", null, null);
        window.onpopstate = function () {
            history.pushState('newjibberish', null, null);
            link_content({'link':'home'});
        };
    }
}