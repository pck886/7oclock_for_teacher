# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from mosu.home.models import UserProfile, Union, Group, GroupUser, UnionUser, School
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','grade','city','region','name','founder','address')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','union','unionuser','title','is_paid')

class UnionAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','address','phone','is_active')

class GroupUserAdmin(admin.ModelAdmin):
    list_display = ('id','group','user','is_active')

class UnionUserAdmin(admin.ModelAdmin):
    list_display = ('id','union','user','is_active')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = True

class UserAdmin(AuthUserAdmin):
    list_display = ('id','Account','username','first_name','Gender','Phone','School','GradeCode','date_joined')
    inlines = [UserProfileInline]
    ordering = ('-id',)

    def Account(self, instance):
        return u"%s"%instance.profile.get_login_from()

    def Gender(self, instance):
        if instance.profile.gender == 0 : return u"남자"
        return u"여자"

    def Phone(self, instance):
        return instance.profile.phone

    def School(self, instance):
        if instance.profile.school:
            return u"%s %d학년"%(instance.profile.school.name, instance.profile.year)
        else :
            return u"없음"

    def GradeCode(self, instance):
        return instance.profile.grade_code

admin.site.register(School, SchoolAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Union, UnionAdmin)
admin.site.register(GroupUser, GroupUserAdmin)
admin.site.register(UnionUser, UnionUserAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)