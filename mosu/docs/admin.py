# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mosu.docs.models import QuestionUnit1, QuestionUnit2, QuestionUnit3, QuestionUnit4, Question, QuestionUnit5, \
    QuestionFeedback


class QuestionUnit1Admin(admin.ModelAdmin):
    list_display = ('id','title','is_active')

class QuestionUnit2Admin(admin.ModelAdmin):
    list_display = ('id','unit','title','is_active')

class QuestionUnit3Admin(admin.ModelAdmin):
    list_display = ('id','unit','title','is_active')

class QuestionUnit4Admin(admin.ModelAdmin):
    list_display = ('id','unit','title','is_active')

class QuestionUnit5Admin(admin.ModelAdmin):
    list_display = ('id','unit','title','is_active')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','type','items','unit','src','explain','keyword','video','answer','answer_mobile','is_active','date_created')

class QuestionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','user','is_good','question')

admin.site.register(QuestionUnit1, QuestionUnit1Admin)
admin.site.register(QuestionUnit2, QuestionUnit2Admin)
admin.site.register(QuestionUnit3, QuestionUnit3Admin)
admin.site.register(QuestionUnit4, QuestionUnit4Admin)
admin.site.register(QuestionUnit5, QuestionUnit5Admin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionFeedback, QuestionFeedbackAdmin)