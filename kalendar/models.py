# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Event(models.Model):

    CSS_CLASS_CHOICES = (
        ('', 'Normal'),
        ('event-warning', 'Warning'),
        ('event-info', 'Info'),
        ('event-success', 'Success'),
        ('event-inverse', 'Inverse'),
        ('event-special', 'Special'),
        ('event-important', 'Important')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('title', max_length=255)
    day = models.DateField('day')
    starting_time = models.TimeField('starting_time')
    ending_time = models.TimeField('ending_time')

    personal_notes = models.TextField('personal_notes', blank=True, null=True)


    class Meta:
        verbose_name = 'scheduling'
        verbose_name_plural = 'scheduling'

    def get_absolute_url(self, user, request=''):

        if not self.id:
            self.id = 0

        if 'admin' not in request:
            url = reverse('modify_event', args=[self.id])
            return '<a href="%s">%s%s</a>' % (url, self.title[:7],'...')


    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def clean(self):
        if self.ending_time <= self.starting_time:
            raise ValidationError('Starting time could not be after ending time')



    def __unicode__(self):
        return self.title
