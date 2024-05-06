# Generated by Django 4.2.7 on 2024-02-04 16:09

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk2heal', '0008_psychologist_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='contact_number',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='psychologist',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]