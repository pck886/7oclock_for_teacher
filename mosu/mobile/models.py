# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from mosu.docs.models import Question

class QuestionInventory(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "문제보관함(QuestionInventory)"

    def __unicode__(self):
        return u'[%d] %s:%s' %(self.id, self.user, self.question)
