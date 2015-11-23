var is_changed = false;
var item_no = 0;
var select_url = '';
var alert_value = {};

$(window).load(function(){
    link_content({'link':'home'});
});

$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip();

    $('input[type=radio], input[type=checkbox]').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });

    function getSearchList(q, grade){
        $('.div_list_school').show();
        $('.div_list_school').load('/home/list/school/',{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            'q':q, 'grade':grade
        });
    }

    $('#div_modal_welcome2 #input_dashboard_ele2_school').focus(function(evt){
        if($("#input_dashboard_ele2_school").val() != "") getSearchList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
    });

    $('#div_modal_welcome2 #input_dashboard_ele2_school').change(function(evt){
        if($("#input_dashboard_ele2_school").val() != "") getSearchList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
        else $('.div_list_school').hide();
    });

    $('#div_modal_welcome2 #input_dashboard_ele2_school').keyup(function(evt){
        getSearchList($('#div_modal_welcome2 #input_dashboard_ele2_school').val(), $('#div_modal_welcome2 #uschoolgrade').val());
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
        var input_maketest_Group = $("#div_modal_maketest #input_maketest_Group").val();
        var input_maketest_title = $("#div_modal_maketest #input_maketest_title").val();
        var select_inventory_year = $("#div_modal_maketest #select_inventory_year > option:selected").val();
        var radio_inventory_purpose = $("#div_modal_maketest input[name=maketest_purpose]:checked").val();
        var questions = "";
        var arr = {};

        if(input_maketest_tpid){
            $("#div_main_loading").show();
            select_url = "/select/post/maketest/";
            arr = {
                'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val(),
                'Group':input_maketest_Group,
                'title':input_maketest_title,
                'year':select_inventory_year,
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
                'Group':input_maketest_Group,
                'title':input_maketest_title,
                'year':select_inventory_year,
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
        if(alert_value.type == "testpaper_group_open"){
            $(alert_value.load_id).load(alert_value.url,alert_value.data,alert_value.function);
        }else if(alert_value.type == "testpaper_delete"){
            $("#div_main_loading").show();
            $(alert_value.load_id).load(alert_value.url,alert_value.data,alert_value.function);
        }else if(alert_value.type == "manager_user_delete"){
            $("#div_main_loading").show();
            $(alert_value.load_id).load(alert_value.url,alert_value.data,alert_value.function);
        }
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
    //    if($("#input_mypage_ele1_now").val() != "") getSearchList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});
    //
    //$('#div_modal_mypage_ele1 #input_mypage_ele1_change').change(function(evt){
    //    getSearchList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});
    //
    //$('#div_modal_mypage_ele1 #input_mypage_ele1_change').keyup(function(evt){
    //    getSearchList($('#div_modal_mypage_ele1 #input_mypage_ele1_change').val());
    //});



});

function alert_show(arr){
    alert_value = arr;
    $("#div_modal_alert .p_page_title").html(alert_value.title);
    $("#div_modal_alert .div_page_contents").html(alert_value.contents);
    $("#div_modal_alert").modal("show");
}

function set_search(){
    var q = $("#input_search_bar").val();
    $("#content").hide().load(select_url+"&q="+q,{
        'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
    }).fadeIn();
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

    if(obj.link == 'home'){
        select_url = "/dashboard/?id=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'inventory'){
        select_url = "/inventory/?year=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'select'){
        select_url = "/select/?unit1=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
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
        },function(data, err){
            $("#div_main_loading").fadeOut();
            // if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'testpaper_modify'){
        select_url = "/testpaper/modify/?unit1=0&tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
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
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'testpaper_similar'){
        select_url = "/testpaper/similar/?tpid="+obj.tpid;
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'progress'){
        select_url = "/progress/?year=0";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'mypage'){
        select_url = "/mypage/?";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
    }else if(obj.link == 'manager'){
        select_url = "/manager/?";
        $("#content").load(select_url,{
            'csrfmiddlewaretoken':$("#wrap > input[name=csrfmiddlewaretoken]").val()
        },function(data, err){
            $("#div_main_loading").fadeOut();
            if(err == "error") location.reload(true);
        });
        $("#wrap #container #div_select_box").hide();
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