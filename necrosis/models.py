from django.db import models


# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=524, blank=True)
    images = models.FileField(upload_to='uploads/')


class Api_Images(models.Model):
	"""docstring for Api_Images"""
	image = models.FileField(upload_to='api_uploads/')
		