# Generated by Django 2.2.5 on 2019-09-18 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='image',
        ),
    ]
