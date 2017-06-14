from django.db import models
from rest_framework import serializers

from pdb import set_trace


# Create your models here.
"""
By default, when a file is uploaded using a FileField or ImageField,
it is saved to a file on a path inside the local directory named by MEDIA_ROOT,
 under a subdirectory named by the field's upload_to value. When the file's url
  attribute is accessed, it returns the value of MEDIA_URL, prepended to the
   file's path inside MEDIA_ROOT.
"""


class BasicPhoto(models.Model):
    image = models.ImageField(upload_to='basic_photo',
                              default='basic_photo/no-img.jpg')


class BasicPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicPhoto
        fields = ('id', 'image')

'''
Album, AlbumPhoto
Example of nested serializer for photos. We want this in case someone wants
multiple photos per model.
'''

'''
Model that represents a photo IN a photo album.
Wrapper like this can be used to associate N photos (albumphoto) with
a parent object (album)
'''
class AlbumPhoto(models.Model):
    image = models.ImageField(upload_to='album_photo',
                              default='album_photo/no-img.jpg')
    creator = models.ForeignKey("auth.User", related_name="+"
      , blank=False, null=False)
    #notes = models.CharField(max_size=1024)
    album = models.ForeignKey("Album", related_name="images"
      , blank=False, null=False)


class AlbumPhotoSerializer(serializers.ModelSerializer):
    # creator = serializers.StringRelatedField(source="creator.username");
    #  image = BasicPhotoSerializer(required=True)


    class Meta:
        model = AlbumPhoto
        fields = ('id', 'image','creator','album') #'notes','creator')

    def create(self, validated_data):
        u = validated_data.pop('creator')

        obj = AlbumPhoto.objects.create(creator=u, **validated_data);
        return obj


class Album(models.Model):
    creator = models.ForeignKey("auth.User", related_name="+"
      , blank=False, null=False)
    notes = models.CharField(max_length=1024)


class AlbumSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source="creator.username")
    images = AlbumPhotoSerializer(many=True)


    class Meta:
        model = Album
        fields = ('id', 'notes','creator','images') #'notes','creator')

    def create(self, validated_data):
        u = validated_data.pop('creator')
        photos_data = validated_data.pop('images')
        obj = Album.objects.create(creator=u,**validated_data)
        for track_data in photos_data:
            AlbumPhoto.objects.create(album=obj, **track_data)
        #set_trace()
        return obj
