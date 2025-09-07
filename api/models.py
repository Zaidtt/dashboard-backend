from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    data = models.JSONField()  # Almacena datos como JSON para flexibilidad (o usa campos dinámicos si prefieres)

class Upload(models.Model):
    file = models.FileField(upload_to='datasets/')  # Para subir nuevos datasets

