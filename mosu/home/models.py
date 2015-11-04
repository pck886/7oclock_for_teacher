# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.
from django.db.models import Count


class School(models.Model):
    title = models.TextField()
    address = models.TextField(null=True,blank=True)
    phone = models.TextField(null=True,blank=True)
    logo = models.FileField(upload_to="upload/",default="static/img/main/default_user.png")
    icon = models.FileField(upload_to="upload/",default="static/img/main/default_user.png")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "학교(School)"

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.title)

    def get_years(self):
        return SchoolYear.objects.filter(school=self).values('year').annotate(Count('year'))

class SchoolYear(models.Model):
    school = models.ForeignKey(School)
    year = models.TextField(default='1')
    room = models.TextField(default='1')

    class Meta:
        verbose_name_plural = "학년반(SchoolYear)"

    def __unicode__(self):
        return u'[%d] %s %s-%s' %(self.id,self.school,self.year,self.room)

    def get_userprofiles(self):
        return UserProfile.objects.filter(schoolyear=self).order_by("user__first_name")

GENDER_IN_PROFILE_CHOICES = (
    (0, u'남자'),
    (1, u'여자'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile")
    gender = models.IntegerField(choices=GENDER_IN_PROFILE_CHOICES,default=0)
    school = models.ForeignKey(School,null=True,blank=True)
    schoolyear = models.ForeignKey(SchoolYear,null=True,blank=True)
    src = models.FileField(upload_to="upload/",null=True,blank=True)
    phone = models.TextField()

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.user.first_name)

    def get_gender(self):
        return GENDER_IN_PROFILE_CHOICES[self.gender][1]

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