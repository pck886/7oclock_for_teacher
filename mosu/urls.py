# -*- coding: utf-8 -*-
"""mosu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mosu import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', 'mosu.home.views.home'),
    url(r'^home/list/school/$', 'mosu.home.views.home_list_school'),
    url(r'^user/$', 'mosu.home.views.user'),
    url(r'^user/login/$', 'mosu.home.views.user_login'),
    url(r'^user/logout/$', 'mosu.home.views.user_logout'),
    url(r'^user/join/$', 'mosu.home.views.user_join'),
    url(r'^user/join/get/$', 'mosu.home.views.user_join_get'),
    url(r'^$', 'mosu.main.views.main'),
    url(r'^inventory/$', 'mosu.main.views.main_inventory'),
    url(r'^select/$', 'mosu.main.views.main_select'),
    url(r'^select/post/maketest/$', 'mosu.main.views.main_select_post_maketest'),
    url(r'^select/post/maketest/chkname/$', 'mosu.main.views.main_select_post_maketest_chkname'),
    url(r'^testpaper/$', 'mosu.main.views.main_testpaper'),
    url(r'^testpaper/modify/$', 'mosu.main.views.main_testpaper_modify'),
    url(r'^testpaper/form/$', 'mosu.main.views.main_testpaper_form'),
    url(r'^testpaper/similar/$', 'mosu.main.views.main_testpaper_similar'),
    url(r'^testpaper/post/delete/$', 'mosu.main.views.main_testpaper_post_delete'),
    url(r'^testpaper/post/modify/$', 'mosu.main.views.main_testpaper_post_modify'),
    url(r'^testpaper/post/similar/$', 'mosu.main.views.main_testpaper_post_similar'),
    url(r'^testpaper/post/form/$', 'mosu.main.views.main_testpaper_post_form'),
    url(r'^testpaper/post/room/$', 'mosu.main.views.main_testpaper_post_room'),
    url(r'^progress/$', 'mosu.main.views.main_progress'),
    url(r'^manager/$', 'mosu.main.views.main_manager'),
    url(r'^manager/post/user/delete/$', 'mosu.main.views.main_manager_post_user_delete'),
    url(r'^mypage/$', 'mosu.main.views.main_mypage'),
    url(r'^main/mypage/post/group/change/$', 'mosu.main.views.main_mypage_post_group_change'),
    url(r'^main/mypage/post/pw/change/$', 'mosu.main.views.main_mypage_post_pw_change'),
    url(r'^main/mypage/post/info/change/$', 'mosu.main.views.main_mypage_post_info_change'),
    url(r'^mobile/$', 'mosu.mobile.views.mobile'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()