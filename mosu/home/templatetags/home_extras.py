# -*- coding: utf-8 -*-
from django.utils.dateformat import format
from mosu.home.models import GroupUser, get_or_none, UnionUser, Group
from mosu.main.models import TestPaperSubmit

__author__ = 'JerryPark'

from django import template

register = template.Library()

@register.filter
def diff(arr, num=0):
    if arr : return range(0,abs(num-len(arr)))
    return range(0,abs(num))

@register.filter
def times(arg, n):
    return int(arg)*int(n)

@register.filter
def set_testpaper_head(html, tp):
    if tp.title : html = html.replace('{{title}}',tp.title)
    if tp.union : html = html.replace('{{logo}}',tp.union.get_logo())
    if tp.union : html = html.replace('{{icon}}',tp.union.get_icon())
    if tp.union : html = html.replace('{{union}}',tp.union.title)
    if tp.title : html = html.replace('{{unit}}',"")
    return html

@register.filter
def set_testpaper_type(html,type):
    if type == "explain" : html = html.replace('{{title}}',u'{{title}}(해설)')
    if type == "answer" : html = html.replace('{{title}}',u'{{title}}(답안)')
    if type == "stats" : html = html.replace('{{title}}',u'{{title}}(통계)')
    return html

@register.filter
def get_testpapersubmit_question(tp, qid):
    return TestPaperSubmit.objects.filter(testpaper=tp,question=qid)

@register.filter
def get_testpapersubmit_group(tps, group):
    if tps and group :
        return tps.filter(testpaper__union=group.unionuser.union)
    return []

@register.filter
def get_submit_percent(tpss):
    count = 0.0
    for tps in tpss :
        if tps.answer != tps.question.answer_mobile :
            count = count + 1.0
    if count > 0.0 : percent = (count/len(tpss))*100.0
    else : percent = 0.0
    return percent

@register.filter
def get_group_checked(ele, testpaper):
    if testpaper.groups.filter(id=ele.id) :
        return True
    return False

@register.filter
def get_groupuser_by_union(user, union):
    arr_list = []
    unionuser = get_or_none(UnionUser,union=union, user=user)
    group = Group.objects.filter(unionuser=unionuser)
    for g in group :
        arr_list.append(g)
    for gu in GroupUser.objects.filter(unionuser=unionuser):
        arr_list.append(gu.group)
    return arr_list

@register.filter
def get_level_by_union(user, union):
    if union.user == user : return 1
    else:
        unionuser = get_or_none(UnionUser,union=union, user=user)
        group = Group.objects.filter(unionuser=unionuser)
        if group : return 2
        else :
            groupuser = GroupUser.objects.filter(unionuser=unionuser)
            if groupuser: return 3
    return 0

@register.filter
def get_title_by_level(level):
    if level == 1 : return "소속 관리자"
    elif level == 2 : return "그룹 관리자"
    elif level == 3 : return "학생"
    else : return "일반인"

@register.filter
def search_user(arr, query):
    if arr :
        return arr.filter(user__first_name__icontains=query)
    return None

@register.filter
def unixtime(value):
    try:
        return format(value, u'U')
    except AttributeError:
        return ''