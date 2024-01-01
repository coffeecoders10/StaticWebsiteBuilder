from django.db import models

# Create your models here.
class Webpages(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    path = models.CharField(max_length=255)
    render_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name
