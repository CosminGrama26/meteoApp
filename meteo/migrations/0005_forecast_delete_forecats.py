# Generated by Django 5.0.2 on 2024-03-22 12:37

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meteo", "0004_forecats_rename_rain_1h_current_weather_rain_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Forecast",
            fields=[
                (
                    "current_weather_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="meteo.current_weather",
                    ),
                ),
                (
                    "f_rain",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=4,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1000),
                        ],
                    ),
                ),
                (
                    "f_snow",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=4,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10000),
                        ],
                    ),
                ),
                ("f_datetime", models.DateTimeField()),
            ],
            bases=("meteo.current_weather",),
        ),
        migrations.DeleteModel(
            name="Forecats",
        ),
    ]
