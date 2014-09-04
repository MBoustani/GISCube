from django.db import models
from giscube.config import MEDIA_URL

class Document(models.Model):
    docfile = models.FileField(upload_to=MEDIA_URL)