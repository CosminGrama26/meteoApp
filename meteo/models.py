from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Update_tracker(models.Model):
    name = models.CharField(max_length=34)
    last_updated = models.DateTimeField(auto_now_add=True)

    def update(self):
        self.last_updated = datetime.now(timezone.utc)
        self.save()

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    latitude = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    name = models.CharField(max_length=34)
    is_county_seat = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Current_weather(models.Model):
    location = models.ForeignKey(
        Location, related_name="current_weather", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    main = models.CharField(max_length=20)
    icon_id = models.CharField(max_length=7)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(-50), MaxValueValidator(70)]                        
    )
    pressure = models.SmallIntegerField(
        validators=[MinValueValidator(900), MaxValueValidator(1100)]
    )
    humidity = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wind_speed = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    wind_direction = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(360)]
    )
    rain = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(350)],
        blank=True, null=True
    )
    snow = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(3500)],
        blank=True, null=True
    )


class Forecast(Current_weather):
    f_rain = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        blank=True, null=True
    )
    f_snow = models.DecimalField(max_digits=4, decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        blank=True, null=True
    )
    f_datetime = models.DateTimeField(auto_now_add=False,
        blank=False, null=False
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name="is_favorite", on_delete=models.CASCADE)