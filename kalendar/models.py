# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from time import mktime
from datetime import datetime


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
    title = models.CharField('title', max_length=255)
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

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.starting_time, event.ending_time, self.starting_time, self.ending_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.starting_time) + '-' + str(event.ending_time))

    def timestamp_to_datetime(self,timestamp):
        if isinstance(timestamp, (str, unicode)):

            if len(timestamp) == 13:
                timestamp = int(timestamp) / 1000

                return datetime.fromtimestamp(timestamp)
            else:
                return ""

    def datetime_to_timestamp(slef,date):
        if isinstance(date, datetime):

            timestamp = mktime(datetime.timetuple())
            json_timestamp = int(timestamp) * 1000

            return '{0}'.format(json_timestamp)
        else:
            return ""
    @property
    def start_timestamp(self):
        return Event.datetime_to_timestamp(self.starting_time)

    @property
    def end_timestamp(self):
        return Event.datetime_to_timestamp(self.end_timestamp)

    def __str__(self):
        return self.title