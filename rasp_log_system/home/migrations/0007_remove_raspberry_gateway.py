# Generated by Django 3.0.5 on 2020-05-05 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_raspberry_gateway'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raspberry',
            name='gateway',
        ),
    ]
