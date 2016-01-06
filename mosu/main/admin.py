# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mosu.main.models import TestPaper, TestPaperQuestion, TestPaperForm, TestPaperSubmit, QnAAnswer, \
    QnAQuestion, QnAQuestionImage, QnAAnswerImage


class TestPaperAdmin(admin.ModelAdmin):
    list_display = ('id','user','union','title','purpose','is_shown','is_exported','date_created')

class TestPaperQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','testpaper','question')

class TestPaperFormAdmin(admin.ModelAdmin):
    list_display = ('id','title','union','html','outline','view','date_created')

class TestPaperSubmitAdmin(admin.ModelAdmin):
    list_display = ('id','user','testpaper','answer','question')

class QnAQuestionImageInline(admin.StackedInline):
    model = QnAQuestionImage
    can_delete = True

class QnAQuestionAdmin(admin.ModelAdmin):
    list_display = ('id','user','unit','contents','date_created')
    inlines = [QnAQuestionImageInline]

class QnAAnswerImageInline(admin.StackedInline):
    model = QnAAnswerImage
    can_delete = True

class QnAAnswerAdmin(admin.ModelAdmin):
    list_display = ('id','user','question','contents','is_selected','date_created')
    inlines = [QnAAnswerImageInline]

admin.site.register(TestPaper, TestPaperAdmin)
admin.site.register(TestPaperQuestion, TestPaperQuestionAdmin)
admin.site.register(TestPaperForm, TestPaperFormAdmin)
admin.site.register(TestPaperSubmit, TestPaperSubmitAdmin)
admin.site.register(QnAQuestion, QnAQuestionAdmin)
admin.site.register(QnAAnswer, QnAAnswerAdmin)