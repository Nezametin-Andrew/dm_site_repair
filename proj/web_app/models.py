from django.db import models


class Quiz(models.Model):

    type = models.CharField(max_length=255, verbose_name='')
    area = models.IntegerField(verbose_name='')
    material = models.CharField(max_length=255, verbose_name='')
    date_repair = models.CharField(max_length=255, verbose_name='')
    name = models.CharField(max_length=255, verbose_name='')
    phone = models.CharField(max_length=255, verbose_name='')
    created_at = models.DateTimeField(auto_now_add=True)