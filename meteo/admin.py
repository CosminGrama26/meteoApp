from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Location)
admin.site.register(models.Current_weather)
admin.site.register(models.Update_tracker)
admin.site.register(models.Forecast)
admin.site.register(models.Favorite)