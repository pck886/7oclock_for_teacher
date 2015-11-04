# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from mosu.home.models import UserProfile, School, SchoolYear
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('id','school','year','room')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','title','address','phone','is_active')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = True

class UserAdmin(AuthUserAdmin):
    list_display = ('id','username','first_name','SchoolYear','Gender','Level','Phone','is_active','date_joined')
    inlines = [UserProfileInline]
    ordering = ('-id',)

    def SchoolYear(self, instance):
        return u"%s"%instance.profile.schoolyear

    def Level(self, instance):
        if instance.profile.school : return u"교사"
        elif instance.profile.schoolyear : return u"학생"
        return u""

    def Gender(self, instance):
        if instance.profile.gender == 0 : return u"남자"
        return u"여자"

    def Phone(self, instance):
        return instance.profile.phone

admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)