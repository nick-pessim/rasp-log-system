# Generated by Django 3.0.3 on 2020-04-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_raspberry'),
    ]

    operations = [
        migrations.AddField(
            model_name='raspberry',
            name='logins',
            field=models.TextField(default=''),
        ),
    ]