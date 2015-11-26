# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from mosu.docs.models import Question
from mosu.home.models import Union, Group


class TestPaperForm(models.Model):
    title = models.TextField(default='')
    union = models.ForeignKey(Union,blank=True,null=True)
    view = models.FileField(upload_to="upload/",default="/static/img/main/default_user.png")
    html = models.TextField(default='')
    outline = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "테스트 서식(TestPaperForm)"

    def __unicode__(self):
        return u'[%d]%s %s' %(self.id, self.union, self.title)

PURPOSE_IN_TESTPAPER_CHOICES = (
    (0, u'테스트용'),
    (1, u'열람용'),
)

class TestPaper(models.Model):
    user = models.ForeignKey(User)
    union = models.ForeignKey(Union)
    title = models.TextField(default='')
    form = models.ForeignKey(TestPaperForm)
    purpose = models.IntegerField(choices=PURPOSE_IN_TESTPAPER_CHOICES,default=0)
    groups = models.ManyToManyField(Group,blank=True)
    is_shown = models.BooleanField(default=True)
    is_exported = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "테스트(TestPaper)"

    def __unicode__(self):
        return u'[%d] %s %s' %(self.id, self.title, self.user)

    def get_submit(self, user):
        return TestPaperSubmit.objects.filter(testpaper=self,user=user)

    def get_purpose(self):
        return PURPOSE_IN_TESTPAPER_CHOICES[self.purpose][1]

    def get_score_user(self, user):
        tpss = TestPaperSubmit.objects.filter(testpaper=self,user=user)
        count = 0.0
        for tps in tpss :
            if tps.question.answer_mobile == tps.answer :
                count = count + 1.0
        if count : score = (count/len(tpss))*100.0
        else : score = 0
        return score

    def get_questions(self):
        arr = []
        tpqs = TestPaperQuestion.objects.filter(testpaper=self).order_by("-id")
        for tpq in tpqs:
            arr.append(tpq.question)
        return arr

class TestPaperQuestion(models.Model):
    testpaper = models.ForeignKey(TestPaper)
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name_plural = "테스트 문제(TestPaperQuestion)"

    def __unicode__(self):
        return u'[%d] %s:%s' %(self.id, self.testpaper, self.question)

class TestPaperSubmit(models.Model):
    user = models.ForeignKey(User)
    testpaper = models.ForeignKey(TestPaper)
    question = models.ForeignKey(Question)
    answer = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name_plural = "제출된 테스트(TestPaperSubmit)"

    def is_answer(self):
        return self.question.answer_mobile == self.answer