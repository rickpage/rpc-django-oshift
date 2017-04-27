from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
from .models import BasicPhoto
from .forms import ImageUploadForm

# Create your views here.
def basic_photo_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        #try:
        if form.is_valid():
            m = BasicPhoto.objects.create()
            m.image = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
        #except NoAuthHandlerFound
    return HttpResponseForbidden('allowed only via POST')
