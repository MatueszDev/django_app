# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Poll(models.Model):

    question = models.CharField('question', max_length=255)
    description = models.CharField('description', default=None, max_length=150)
    publication_date = models.DateField('publication_date', default=now)


    def __unicode_(self):
        return self.question


class Respond(models.Model):

    option = models.CharField('option', max_length=255)
    poll = models.ForeignKey(Poll)

    def __unicode_(self):
        return self.option


class Vote(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Respond)

    @staticmethod
    def count_all_votes():
        number_of_votes = Vote.objects.all().count()
        return number_of_votes

    @staticmethod
    def count_option_votes(option):
        number_of_votes = Vote.objects.filter(option= option).count()
        return  number_of_votes