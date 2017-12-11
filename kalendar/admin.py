# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Event
import datetime
import calendar
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from utils import Calendar

class EventAdmin(admin.ModelAdmin):
    list_display = ['title','day', 'starting_time', 'ending_time', 'personal_notes']
    change_list_template = 'admin/kalendar/change_list.html'

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}


        if not after_day:
            day = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                day = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]),day=1)
            except:
                day = datetime.date.today()

        previous_month = datetime.date(year=day.year, month=day.month, day=1)
        previous_month -= datetime.timedelta(days=1)
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month, day=1)

        last_day = calendar.monthrange(day.year, day.month)
        next_month = datetime.date(year=day.year, month=day.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

        extra_context['previous_month'] = reverse('admin:kalendar_event_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:kalendar_event_changelist') + '?day__gte=' + str(next_month)
        cal = Calendar()
        html_calendar = cal.formatmonth(day.year, day.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td width="100" height="100"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventAdmin, self).changelist_view(request, extra_context)

admin.site.register(Event, EventAdmin)
