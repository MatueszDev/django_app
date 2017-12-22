from calendar import HTMLCalendar
from datetime import datetime
from django import template
from .models import Event
from django.core.files import File

class Calendar(HTMLCalendar):
    def __init__(self, events=None, request='admin'):
        super(Calendar, self).__init__()
        self.events = events
        self.request = request

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url(self.request) + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, user, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(user=user,day__month=themonth, day__year=theyear)


        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month" style="width:100% !important;">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)




class Import():
    def __init__(self, file, content, user):
        self.file = getattr(file, 'name', None)
        self.content = content.readlines()
        self.user = user

    def check_right_name(self):
        if '.csv' not in self.file:
            raise NameError("The file must be csv file")

    def check_right_content(self):
        test_case = ("Name", "Section", "Title", "Approved","Type","Day Of Week","First Date","Last Date")
        for case in test_case:
            if case not in self.content[0]:
                raise IOError('The file includes wrong content')

    def save_events(self):
        all_user_objects = Event.objects.filter(user=self.user)
        for line in self.content[1:]:
            line = line.split(',')

            if len(line) > 12:
                obj = Event()
                obj.user = self.user
                obj.title = line[3].replace('"','')
                obj.day = datetime.strptime(line[5].replace('"',''), '%d.%m.%Y').strftime('%Y-%m-%d')
                obj.starting_time = line[7].replace('"','')
                obj.ending_time = line[8].replace('"','')
                if all_user_objects.filter(day=obj.day , starting_time=obj.starting_time).exists():
                    continue
                #if (obj.ending_time > obj.starting_time):
                #    raise ArithmeticError('Starting time must be elier than ending')
                obj.personal_notes = '%s \n %s \n %s' % (line[9].replace('"',''), line[11].replace('"',''), line[12].replace('"',''))

                try:
                    obj.save()
                except:
                    pass
                else:
                      continue
