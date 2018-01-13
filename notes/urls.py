from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.choose_class, name='choose_class'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/$', views.select_lecture, name='select_lecture'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_note/$', views.add_note, name='add_note'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_file/$', views.add_file, name='add_file'),
    url(r'^add_lecture/$', views.add_lecture, name='add_lecture'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/ask/$', views.add_question, name='add_question'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/(?P<qpk>[0-9]+)/$', views.view_question, name='view_question'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/(?P<qpk>[0-9]+)/ok/$', views.question_okay, name='question_okay'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/(?P<qpk>[0-9]+)/delete/$', views.question_delete, name='question_delete'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/(?P<qpk>[0-9]+)/(?P<rpk>[0-9]+)/delete/$', views.reply_delete, name='reply_delete'),
    url(r'^bookmarks/$', views.bookmarks, name='bookmarks'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/mark/$', views.note_bookmark, name='note_bookmark'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<noteslug>[A-Za-z0-9-]+)/unmark/$', views.note_unmark, name='note_unmark'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<filetype>[tipo])/(?P<filepk>[0-9]+)/mark/$', views.file_bookmark, name='file_bookmark'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/(?P<filetype>[tipo])/(?P<filepk>[0-9]+)/unmark/$', views.file_unmark, name='file_unmark'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_ocr/$',
        views.add_ocr, name='add_ocr'),
    url(r'^(?P<classes>[A-Za-z0-9-]+)/(?P<lecture_number>[0-9]+)/add_crop/$',
        views.add_crop, name='add_crop'),
]
