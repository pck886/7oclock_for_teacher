# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mosu.main.models import TestPaper, TestPaperQuestion, TestPaperForm, TestPaperSubmit


class TestPaperAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','school','year','purpose','is_shown','is_exported','date_created')

class TestPaperQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','testpaper','question')

class TestPaperFormAdmin(admin.ModelAdmin):
    list_display = ('id','title','school','html','outline','view','date_created')

class TestPaperSubmitAdmin(admin.ModelAdmin):
    list_display = ('id','user','testpaper','answer','question')

admin.site.register(TestPaper, TestPaperAdmin)
admin.site.register(TestPaperQuestion, TestPaperQuestionAdmin)
admin.site.register(TestPaperForm, TestPaperFormAdmin)
admin.site.register(TestPaperSubmit, TestPaperSubmitAdmin)