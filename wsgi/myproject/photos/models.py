from django.db import models

# Create your models here.
"""
By default, when a file is uploaded using a FileField or ImageField,
it is saved to a file on a path inside the local directory named by MEDIA_ROOT,
 under a subdirectory named by the field's upload_to value. When the file's url
  attribute is accessed, it returns the value of MEDIA_URL, prepended to the
   file's path inside MEDIA_ROOT.
"""
class BasicPhoto(models.Model):
    image = models.ImageField(upload_to = 'basic_photo', default = 'basic_photo/no-img.jpg')
