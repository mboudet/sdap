import datetime
import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  User
from django.conf import settings

from django.dispatch import receiver

# Create your models here.
class Tag(models.Model):
    word        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.word


class Folder(models.Model):

    name = models.CharField(max_length=200)
    folder = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_updated_by')

    def __str__(self):
        return self.name


class File(models.Model):

    FILE_TYPE = (
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('CSV', 'Csv'),
        ('PDF', 'Pdf'),
        ('RDATA', 'RDdata'),
        ('EXPRESSION_MATRIX', 'Expression matrix'),
    )

    SEP_TYPE = (
        ('\t', 'Tab'),
        (',', 'Comma'),
        (';', 'Semicolon'),
        (' ', 'Space'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField("description", blank=True)
    type = models.CharField(max_length=50, choices=FILE_TYPE, default="TEXT")
    file = models.FileField(upload_to='files/')
    sep_type = models.CharField(max_length=50, choices=SEP_TYPE, default=",")
    folder = models.ForeignKey(Folder, blank=True, null=True, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=("user"))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_updated_by')
    tags = models.ManyToManyField(Tag, related_name='file_tag_description')

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

# Delete in case of update
@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
