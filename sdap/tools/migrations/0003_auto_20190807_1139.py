# Generated by Django 2.0.13 on 2019-08-07 11:39

from django.db import migrations
from sdap.tools.models import ArgumentType

def load_args_type(apps, schema_editor):
    choices = ['Text']

    for choice in choices:
        argument_type = ArgumentType(type=choice)
        argument_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_auto_20190807_1139'),
    ]

    operations = [
        migrations.RunPython(load_args_type),
    ]
