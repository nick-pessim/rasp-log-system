# Generated by Django 3.0.3 on 2020-04-21 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='last_ip',
            new_name='login_ip',
        ),
    ]