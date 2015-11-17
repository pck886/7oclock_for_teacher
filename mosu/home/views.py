# -*- coding: utf-8 -*-
import urllib2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from mosu.home.models import UserProfile, Group, get_or_none, School


def home(request):
    if request.user.id :
        return HttpResponseRedirect('/')
    context = {
        'user': request.user,
        'appname':'home'
    }
    return render(request, 'home.html', context)

def home_list_school(request):
    q = request.POST.get("q","")
    grade = request.POST.get("grade","")
    if q != "": schools = School.objects.filter(name__contains=q,grade=grade)
    else : schools = None
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
    come_from = request.POST.get("come_from",'/')
    login_from = int(request.POST.get("login_from",0))

    if login_from != 0 :
        password = "%d_%s"%(login_from,password)

    user = authenticate(username=userid, password=password)
    if user :
        login(request, user)
        request.session.set_expiry(31536000)
        return HttpResponseRedirect(come_from)
    return HttpResponseRedirect(come_from, status=401)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/')

def user_join(request):
    login_from = int(request.POST.get("login_from", 0))
    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    user_name = request.POST.get("user_name")
    user_email = request.POST.get("user_email")
    gender = int(request.POST.get("user_gender",0))
    img_url = request.POST.get("img_url","")

    profile_img = None
    if login_from != 0 :
        password = "%d_%s"%(login_from,password)
        if img_url :
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(img_url).read())
            img_temp.flush()

    try :
        user = User.objects.create_user(username=user_id,password=password,email=user_email,first_name=user_name)
        if user :
            profile = UserProfile.objects.create(user=user,gender=gender,login_from=login_from)
            profile.src.save("%s.jpg"%user_id, File(img_temp))
            user = authenticate(username=user_id, password=password)
            if user :
                login(request, user)
                request.session.set_expiry(31536000)
                return HttpResponseRedirect('/home/')
    except Exception as e:
        pass
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