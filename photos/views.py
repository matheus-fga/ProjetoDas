from django.shortcuts import render
from django.http import HttpResponseRedirect
from photos.forms import ImageForm
from photos.models import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    image_list = Image.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(image_list, 10)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    return render(request, 'core/image_list.html', { 'images': images })


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


    