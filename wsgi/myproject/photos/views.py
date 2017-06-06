from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseBadRequest
from .models import BasicPhoto, BasicPhotoSerializer
from .forms import ImageUploadForm
from rest_framework import viewsets
from rest_framework.decorators import detail_route, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from pdb import set_trace

@csrf_exempt
def basic_photo_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = BasicPhoto.objects.create()
            m.image = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
        else:
            return HttpResponseBadRequest('Invalid data in form')
    else:
        return HttpResponseForbidden('allowed only via POST')


class BasicPhotoViewSet(viewsets.ModelViewSet):
    queryset = BasicPhoto.objects.all()
    serializer_class = BasicPhotoSerializer
    # permission_classes = (IsAdminOrIsSelf,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @detail_route(methods=['POST'], permission_classes=[])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        if 'image' in request.data:
            user_profile = self.get_object()
            user_profile.image.delete()

            upload = request.data['image']

            user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': user_profile.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
