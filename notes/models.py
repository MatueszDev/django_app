# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Note(models.Model):
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

