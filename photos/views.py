from django.shortcuts import render
from django.http import HttpResponseRedirect
from photos.forms import *


def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = ImageForm()
    return render(request, 'image_upload.html', {'form': form })