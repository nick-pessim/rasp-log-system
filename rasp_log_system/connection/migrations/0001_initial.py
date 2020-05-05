# Generated by Django 3.0.5 on 2020-05-05 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('nome', models.TextField()),
                ('password', models.TextField()),
                ('enable', models.TextField()),
                ('community', models.TextField()),
                ('snmp_vers', models.TextField()),
            ],
        ),
    ]
