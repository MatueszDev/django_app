# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Poll, Respond, Vote
# Register your models here.

class PollAdmin(admin.ModelAdmin):

    list_display = ["question", "description", "publication_date"]

admin.site.register(Poll, PollAdmin)
admin.site.register(Respond)
admin.site.register(Vote)