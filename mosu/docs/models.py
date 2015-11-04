# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class QuestionUnit1(models.Model):
    title = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "1.학년(QuestionUnit1)"

    def __unicode__(self):
        return u'%s' %(self.title)

class QuestionUnit2(models.Model):
    unit = models.ForeignKey(QuestionUnit1)
    title = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "2.대단원(QuestionUnit2)"

    def __unicode__(self):
        return u'%s > %s' %(self.unit.title,self.title)

    def get_questions(self):
        return Question.objects.filter(unit__unit__unit__unit=self)

class QuestionUnit3(models.Model):
    unit = models.ForeignKey(QuestionUnit2)
    title = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "3.중단원(QuestionUnit3)"

    def __unicode__(self):
        return u'%s > %s > %s' %(self.unit.unit.title,self.unit.title,self.title)

class QuestionUnit4(models.Model):
    unit = models.ForeignKey(QuestionUnit3)
    title = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "4.소단원(QuestionUnit4)"

    def __unicode__(self):
        return u'%s > %s > %s > %s' %(self.unit.unit.unit.title,self.unit.unit.title,self.unit.title,self.title)

class QuestionUnit5(models.Model):
    unit = models.ForeignKey(QuestionUnit4)
    title = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "5.대표유형(QuestionUnit5)"

    def __unicode__(self):
        return u'%s > %s > %s > %s > %s' %(self.unit.unit.unit.unit.title,self.unit.unit.unit.title,self.unit.unit.title,self.unit.title,self.title)

TYPE_IN_QUESTION_CHOICES = (
    (0, u'대표유형'),
    (1, u'일반유형'),
)


class Question(models.Model):
    type = models.IntegerField(choices=TYPE_IN_QUESTION_CHOICES, default=0)
    items = models.IntegerField(default=1)
    unit = models.ForeignKey(QuestionUnit5)
    src = models.ImageField(upload_to="upload/")
    explain = models.ImageField(upload_to="upload/",blank=True,null=True)
    keyword = models.TextField(blank=True,null=True)
    video = models.TextField(blank=True,null=True)
    answer = models.TextField(blank=True,null=True)
    answer_mobile = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "문제(Question)"

    def __unicode__(self):
        return u'[%d]%s, KEYWORD:%s, IS_ACTIVE:%s' %(self.id, self.unit, self.keyword, self.is_active)

    def get_unit_questions(self):
        questions = Question.objects.filter(unit=self.unit,type=0)
        return questions

    def get_answer(self):
        return "$%s$"%self.answer

class QuestionFeedback(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    is_good = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "문제 난이도(QuestionFeedback)"

    def __unicode__(self):
        return u'[%d] %s:%s %s' %(self.id, self.user, self.question, self.is_good)