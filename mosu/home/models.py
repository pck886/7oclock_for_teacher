# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.

GRADE_IN_SCHOOL_CHOICES = (
    (u'초등학교', u'초등학교'),
    (u'중학교', u'중학교'),
    (u'고등학교', u'고등학교'),
    (u'대학교', u'대학교'),
)

class School(models.Model):
    grade = models.CharField(max_length=10,default='중학교',choices=GRADE_IN_SCHOOL_CHOICES)
    city = models.CharField(max_length=10,default='')
    government = models.CharField(max_length=20,default='')
    region = models.CharField(max_length=10,default='')
    name = models.CharField(max_length=128,default='')
    founder = models.CharField(max_length=8,default='')
    zipcode =  models.CharField(max_length=8,default='')
    address =  models.CharField(max_length=256,default='')
    phone =  models.CharField(max_length=30,default='')
    logo = models.FileField(upload_to="upload/",null=True,blank=True)

    class Meta:
        verbose_name_plural = "전국학교(School)"

    def __unicode__(self):
        return u'[%d] %s (%s)' %(self.id,self.name,self.address)

class Union(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=64)
    address = models.CharField(max_length=128,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True,default='-')
    logo = models.FileField(upload_to="upload/",null=True,blank=True)
    icon = models.FileField(upload_to="upload/",null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "소속(Union)"

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.title)

    def get_groups(self):
        return Group.objects.filter(union=self)

    def get_unionusers(self):
        return UnionUser.objects.filter(union=self)

    def get_logo(self):
        if self.logo :
            return self.logo.url
        return "/static/img/main/logo_union_tmp.png"

    def get_icon(self):
        if self.icon :
            return self.icon.url
        return "/static/img/main/icon_union_tmp.png"

class UnionUser(models.Model):
    union = models.ForeignKey(Union)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "소속 사용자(UnionUser)"

    def __unicode__(self):
        return u'[%d] %s > %s' %(self.id,self.union,self.user)

class Group(models.Model):
    union = models.ForeignKey(Union)
    unionuser = models.ForeignKey(UnionUser)
    title = models.CharField(max_length=64)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "그룹(Group)"

    def __unicode__(self):
        return u'[%d] %s %s' %(self.id,self.union,self.title)

    def get_users(self):
        gu = GroupUser.objects.filter(group=self).values_list("unionuser__user")
        return User.objects.filter(id__in=gu)

class GroupUser(models.Model):
    group = models.ForeignKey(Group)
    unionuser = models.ForeignKey(UnionUser)

    class Meta:
        verbose_name_plural = "그룹 사용자(GroupUser)"

    def __unicode__(self):
        return u'[%d] %s > %s' %(self.id,self.group,self.unionuser)

GENDER_IN_PROFILE_CHOICES = (
    (0, u'남성'),
    (1, u'여성'),
)

LOGIN_FROM_IN_PROFILE_CHOICES = (
    (0, u'자체계정'),
    (1, u'Facebook'),
    (2, u'Kakao'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile")
    gender = models.IntegerField(choices=GENDER_IN_PROFILE_CHOICES,default=0)
    src = models.FileField(upload_to="upload/",null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True,default='-')
    school = models.ForeignKey(School,null=True,blank=True)
    year = models.IntegerField(default=1)
    login_from = models.IntegerField(choices=LOGIN_FROM_IN_PROFILE_CHOICES,default=0)
    grade_code = models.CharField(max_length=3,null=True,blank=True)

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.user.first_name)

    def get_login_from(self):
        return u"%s"%LOGIN_FROM_IN_PROFILE_CHOICES[self.login_from][1]

    def get_gender(self):
        return u"%s"%GENDER_IN_PROFILE_CHOICES[self.gender][1]

    def get_unions(self):
        uu = UnionUser.objects.filter(user=self.user).values_list("union__id")
        return Union.objects.filter(id__in=uu,is_active=True)

    # def get_groups(self):
    #     gu = GroupUser.objects.filter(user=self.user,in_group=True).values_list("group")
    #     return Group.objects.filter(id__in=gu)

    def get_grade(self):
        str_grade = ""
        grade = self.grade_code[:1]
        code = self.grade_code[1:2]

        if grade != "n":
            if grade == "m" : str_grade = u"중"
            elif grade == "h" : str_grade = u"고"

            if code == "1" : str_grade = u"%s1"%str_grade
            elif code == "2" : str_grade = u"%s2"%str_grade
            elif code == "3" : str_grade = u"%s3"%str_grade

            return str_grade
        return u"일반인"

    def get_src(self):
        if self.src :
            return self.src.url
        if self.gender == 0 : return "/static/img/main/default_user.png"
        else : return "/static/img/main/default_user_f.png"

def get_or_none(model,order=None, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except MultipleObjectsReturned as e:
        if order == "-":
            res = model.objects.filter(**kwargs).order_by("-id")
        else :
            res = model.objects.filter(**kwargs).order_by("id")
        if res:
            return res[0]
        return None
    except Exception as e:
        return None