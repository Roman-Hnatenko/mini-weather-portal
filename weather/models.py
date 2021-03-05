from django.db import models


class Weather(models.Model):
    city = models.CharField('City', max_length=15)
    description = models.CharField('Description', max_length=15)
    temperature = models.FloatField(default=0)
    wind = models.FloatField(default=0)
    image = models.CharField('Id image', max_length=30, default='')
