from django.db import models

# Create your models here.


class WeatherInformation(models.Model):
    time = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    temperature = models.IntegerField()
    icon = models.CharField(max_length=100)
    link = models.URLField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind = models.FloatField()
    sunrise_timestamp = models.CharField(max_length=10)
    sunset_timestamp = models.CharField(max_length=10)
    duration_of_the_day = models.DurationField()

    # def __str__(self):
        # return self.name
