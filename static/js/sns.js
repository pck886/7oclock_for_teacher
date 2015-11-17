// 사용할 앱의 JavaScript 키를 설정해 주세요.
Kakao.init('8ddcddaf1ccea16f66c25602fb3a9f24');
function loginWithKakao() {
    // 로그인 창을 띄웁니다.
    Kakao.Auth.login({
        success: function(authObj) {
            Kakao.API.request({
                url: '/v1/user/me',
                success: function(res) {
                    $.ajax({
                        type: "POST",
                        url: "/user/login/",
                        data: {
                            'csrfmiddlewaretoken': $("#wrap > input[name=csrfmiddlewaretoken]").val(),
                            'user_id': res.id,
                            'password': res.id,
                            'login_from':2,
                            'come_from': '/'
                        },
                        success: function(msg){
                            document.location.reload();
                        },
                        error: function (XMLHttpRequest, textStatus, errorThrown) {
                            signupWithKakao();
                        }
                    });
                },
                fail: function(error) {
                    alert(JSON.stringify(error))
                }
            });
        },
        fail: function(err) {
            alert(JSON.stringify(err))
        }
    });
}

function signupWithKakao() {
    // 로그인 창을 띄웁니다.
    Kakao.Auth.login({
        success: function(authObj) {
            Kakao.API.request({
                url: '/v1/user/me',
                success: function(res) {
                    $("#div_join_account #login_from").val("2");
                    $("#div_join_account #img_url").val(res.properties.profile_image);
                    $("#div_join_account #uid").val(res.id);
                    $("#div_join_account #upw").val(res.id);
                    $("#div_join_account #upw_").val(res.id);
                    $("#div_join_account #uname").val(res.properties.nickname);
                    $("#div_join_account #uemail").val("@");
                    $("#div_join_account #ugender_0").attr('checked','checked');
                    $("#div_join_account #ugender_1").removeAttr('checked');
                    $("#JoinModal #form_join").submit();
                },
                fail: function(error) {
                    alert(JSON.stringify(error))
                }
            });
        },
        fail: function(err) {
            alert(JSON.stringify(err))
        }
    });
}

function checkLoginState() {
    console.log('checkLoginState');
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}

function fb_signup(){
    FB.login(function(response) {
        console.log(response);
        if (response.status === 'connected') {
            FB.api('/me?fields=id,name,gender,email', {locale : 'ko_KR'}, function(response) {
                $("#div_join_account #login_from").val("1");
                $("#div_join_account #img_url").val("http://graph.facebook.com/"+response.id+"/picture?type=large");
                $("#div_join_account #uid").val(response.id);
                $("#div_join_account #upw").val(response.id);
                $("#div_join_account #upw_").val(response.id);
                $("#div_join_account #uname").val(response.name);
                $("#div_join_account #uemail").val(response.email);
                if(response.gender == '남성'){
                    $("#div_join_account #ugender_0").attr('checked','checked');
                    $("#div_join_account #ugender_1").removeAttr('checked');
                }else{
                    $("#div_join_account #ugender_1").attr('checked','checked');
                    $("#div_join_account #ugender_0").removeAttr('checked');
                }

                $("#JoinModal #form_join").submit();
            });
        } else if (response.status === 'not_authorized') {
            console.log('Please log ' +
                'into this app.');
        } else {
            console.log('Please log ' +
                'into Facebook.');
        }
    });
}

function fb_login(){
    FB.login(function(response) {
        console.log(response);
        if (response.status === 'connected') {
            FB.api('/me?fields=id,name,gender,email', {locale : 'ko_KR'}, function(response) {
                $.ajax({
                    type: "POST",
                    url: "/user/login/",
                    data: {
                        'csrfmiddlewaretoken': $("#wrap > input[name=csrfmiddlewaretoken]").val(),
                        'user_id': response.id,
                        'password': response.id,
                        'login_from':1,
                        'come_from': '/'
                    },
                    success: function(msg){
                        document.location.reload();
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        fb_signup();
                    }
                });
            });
        } else if (response.status === 'not_authorized') {
            console.log('Please log ' +
                'into this app.');
        } else {
            console.log('Please log ' +
                'into Facebook.');
        }
    });
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '420252064830211',
        cookie     : true,
        xfbml      : true,
        version    : 'v2.2',
        email: true
    });

    //FB.getLoginStatus(function(response) {
    //    statusChangeCallback(response);
    //});

    FB.Event.subscribe('auth.logout', function(response) {
        document.location.reload();
    });

};

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/ko_KR/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));