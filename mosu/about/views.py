# -*- coding: utf-8 -*-
from django.shortcuts import render
from mosu.home.models import School

# Create your views here.
def about(request):
    schools = School.objects.all
    context = {
        'user':request.user,
        'schools':schools
    }
    return render(request, 'about.html', context)

def campaign(request):
    address = request.POST.get("address")
    fromNm = request.POST.get("fromNm")
    toNm = request.POST.get("toNm")

    context = {
        'user' : request.user,
    }

    return render(request, 'about.html', context)