import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  User, Group
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps

# Create your models here.

class ExpressionData(models.Model):

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')

    def __str__(self):
        return self.name


class ExpressionStudy(models.Model):

    article = models.CharField(max_length=200)
    pmid = models.CharField(max_length=20)
    ome = models.CharField(max_length=200, blank=True, null=True)
    technology = models.CharField(max_length=200, blank=True, null=True)
    species = models.CharField(max_length=50, blank=True, null=True)
    experimental_design = models.CharField(max_length=200, blank=True, null=True)
    topics = models.TextField("Biological topics", blank=True, null=True)
    tissues = models.TextField("Tissue/Cells", blank=True, null=True)
    sex = models.CharField(max_length=200, blank=True, null=True)
    dev_stage = models.CharField(max_length=200, blank=True, null=True)
    age = models.CharField(max_length=200, blank=True, null=True)
    antibody = models.CharField(max_length=200, blank=True, null=True)
    mutant = models.CharField(max_length=200, blank=True, null=True)
    cell_sorted = models.CharField(max_length=200, blank=True, null=True)
    keywords = models.TextField("Keywords", blank=True, null=True)
    samples_count = models.IntegerField()
    data = models.ManyToManyField(ExpressionData, related_name="studies")

    def __str__(self):
        return self.pmid
