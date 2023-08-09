from django.db import models

# Create your models here.

class Insta(models.Model):
    content = models.TextField(null=False)
    date = models.CharField(null=False, max_length=10)
    like = models.IntegerField(null=False, default=0)
    place = models.CharField(null=False, max_length=100)
    tags = models.TextField(null=False)
    create_date = models.DateTimeField(auto_now_add=True)