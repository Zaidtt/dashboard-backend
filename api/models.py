from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    data = models.JSONField()  # Guarda los datos del CSV en JSON

class Upload(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

