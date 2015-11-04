# -*- coding: utf-8 -*-
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
    if tp.school : html = html.replace('{{logo}}',tp.school.logo.url)
    if tp.school : html = html.replace('{{icon}}',tp.school.icon.url)
    if tp.school : html = html.replace('{{school}}',tp.school.title)
    if tp.title : html = html.replace('{{unit}}',"")
    if tp.year : html = html.replace('{{year}}',"%s"%tp.year)
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
def get_testpapersubmit_room(tps, room):
    return tps.filter(user__profile__schoolyear=room)

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
def get_room_checked(ele, testpaper):
    if testpaper.rooms.filter(id=ele.id) :
        return True
    return False

@register.filter
def search_user(arr, query):
    if arr :
        return arr.filter(user__first_name__icontains=query)
    return None