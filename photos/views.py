from django.shortcuts import render
from django.http import HttpResponseRedirect
from photos.forms import ImageForm
from photos.models import Image


def image_upload(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin/?next=%s' % request.path)
    else:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                return HttpResponseRedirect("/photos/")
        else:
            form = ImageForm()

    images = Image.objects.filter(user=request.user)
    return render(request, 'image_upload.html', {'form': form, 'images': images})


    