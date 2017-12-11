from django.contrib import admin
from .models import Classes, Field_of_study, Year, Grades_group

admin.site.register(Year)
admin.site.register(Field_of_study)
admin.site.register(Classes)
admin.site.register(Grades_group)
