# Generated by Django 2.2.5 on 2019-09-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressionstudy',
            name='samples_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
