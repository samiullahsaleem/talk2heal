# Generated by Django 4.2.7 on 2024-02-04 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk2heal', '0010_patient_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
    ]
