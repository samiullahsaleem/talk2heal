# Generated by Django 4.2.7 on 2024-02-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk2heal', '0012_appointment_chat_link_appointment_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='time_slot',
            field=models.CharField(default='', max_length=255),
        ),
    ]
