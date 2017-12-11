# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
<<<<<<< HEAD
=======
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    subjects = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return 'User account {}.'.format(self.user.username)
>>>>>>> 188f94952a25c2fd10b4546696bff60dbd8f3d8f
