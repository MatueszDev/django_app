from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget, TimeInput
import datetime
from django.core.exceptions import ValidationError

'''def clean(time):
    time_format= "%H:%M:%S"

    try:
        datetime.datetime.strptime(time, time_format)
    except:
        raise ValidationError(
            'Proper format hh:mm:ss',
        )
'''

class EventForm(forms.Form):
    title = forms.CharField(label='Title of event' ,max_length=255)
    day = forms.DateField(label='date', widget=SelectDateWidget(empty_label="Nothing"))
    starting_time = forms.TimeField(label='start', widget=forms.TextInput({ "placeholder": "12:00" }))
    ending_time = forms.TimeField(label='end', widget=forms.TextInput({ "placeholder": "13:30" }))

    personal_notes = forms.CharField( label='notes',widget=forms.Textarea, required=False)

