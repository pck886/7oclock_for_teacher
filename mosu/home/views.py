# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from mosu.home.models import UserProfile, School, get_or_none


def home(request):
    if request.user.id :
        return HttpResponseRedirect('/')
    context = {
        'user': request.user,
        'appname':'home'
    }
    return render(request, 'home.html', context)

def home_list_school(request):
    q = request.POST.get("q")
    schools = School.objects.filter(title__contains=q,is_active=True)
    context = {
        'user': request.user,
        'schools':schools
    }
    return render(request, 'home_list_school.html', context)

def user(request):
    return HttpResponse("%s"%request.user.first_name)

def user_login(request):
    userid = request.POST.get("user_id")
    password = request.POST.get("password")
    come_from = request.POST.get("come_from")
    user = authenticate(username=userid, password=password)
    if user and user.profile.school :
        login(request, user)
        request.session.set_expiry(31536000)
        return HttpResponseRedirect(come_from)
    return HttpResponseRedirect(come_from)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/')

def user_join(request):
    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    user_name = request.POST.get("user_name")
    user_email = request.POST.get("user_email")
    phone = request.POST.get("user_phone")
    gender = int(request.POST.get("user_gender",0))
    school = request.POST.get("school_id")
    if school : school = get_or_none(School,id=school)
    user = User.objects.create_user(username=user_id,password=password,email=user_email,first_name=user_name)
    if user :
        UserProfile.objects.create(user=user,phone=phone,school=school,gender=gender)
        user = authenticate(username=user_id, password=password)
        if user :
            if user.profile.gender == 0 : user.profile.src = "default_user.png"
            else : user.profile.src = "default_user_f.png"
            user.profile.save()

            login(request, user)
            request.session.set_expiry(31536000)
            return HttpResponseRedirect('/home/')
    return HttpResponseRedirect('/home/')

def user_join_get(request):
    userid = request.POST.get("userid")
    email = request.POST.get("email")
    if userid :
        query = User.objects.filter(username=userid)
        if query :
            return HttpResponse(0);
    elif email :
        query = User.objects.filter(email=email)
        if query :
            return HttpResponse(0);
    return HttpResponse(1);