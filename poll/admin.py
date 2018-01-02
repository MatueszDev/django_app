# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Poll, Respond, Vote
# Register your models here.

class PollAdmin(admin.ModelAdmin):

    list_display = ["question", "description", "publication_date"]


class RespondAdmin(admin.ModelAdmin):

    list_display = ["option", "poll"]

class VoteAdmin(admin.ModelAdmin):

    list_display = ["user", "poll", "choice"]

admin.site.register(Poll, PollAdmin)
admin.site.register(Respond, RespondAdmin)
admin.site.register(Vote, VoteAdmin)