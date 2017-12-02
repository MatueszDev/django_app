# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

class Event(models.Model):
    day = models.DateField('day')
    starting_time = models.TimeField('starting_time')
    ending_time = models.TimeField('ending_time')
    personal_notes = models.TextField('personal_notes', blank=True, null=True)


    class Meta:
        verbose_name = 'scheduling'
        verbose_name_plural = 'scheduling'

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.starting_time))

    def time_sentinel(self):
        if self.ending_time <= self.starting_time:
            raise ValidationError('Starting time could not be after ending time')