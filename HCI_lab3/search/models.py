from django.db import models

# Create your models here.
class SearchImage(models.Model):
	search_img=models.FileField(upload_to='./upload/')