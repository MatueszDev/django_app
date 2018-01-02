# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from ocr.scripts.ocr_pytesseract import scanner

from django.http import HttpResponseRedirect
from .forms import UploadForm
from django.template.context_processors import csrf
from django.shortcuts import render_to_response

from .models import Scanned

def index(request): #test only
    print(Scanned.objects.all())
    return render(request, 'ocr_main.html', {'scanned': Scanned.objects.all()})

#def scan(request): #not used, but exists in urls
#    path = 'ocr/scripts/page.jpg'
#    scanner(path)
#    return HttpResponse("scan")

def add_image(request): 
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            tmp = scanner(request.FILES['file'])
            Scanned.objects.create(name = "test", content = tmp)
            #scanned_instance = Scanned.objects.create(content = scanner(request.FILES['file']))
            #form.save()
            return HttpResponseRedirect('/ocr/')
    else:
        form = UploadForm(request.POST)
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('add_image_ocr.html', args)



