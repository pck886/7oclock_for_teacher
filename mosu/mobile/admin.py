# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mosu.mobile.models import QuestionInventory


class QuestionInventoryAdmin(admin.ModelAdmin):
    list_display = ('id','user','question','date_created')

admin.site.register(QuestionInventory, QuestionInventoryAdmin)