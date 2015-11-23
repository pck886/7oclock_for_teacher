# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
def about(request):
    context = {
        'user':request.user,
    }
    return render(request, 'about.html', context)