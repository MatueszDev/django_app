# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Scanned(models.Model):
    '''Model for notes stored as plaintext (default)'''
    name = models.CharField(max_length = 100)
    content = models.TextField(max_length=100000)

    def __unicode__(self):
        return self.name
