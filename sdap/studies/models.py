import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import  User, Group
from django_better_admin_arrayfield.models.fields import ArrayField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.apps import apps

import sys
import pickle, os

class ExpressionData(models.Model):

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ExpressionData, self).save(*args, **kwargs)
        dIndex={'Sample':0}
        with self.file.file.open('r') as f:
            for line in f.readlines():
                sIdList = line.decode().rstrip().split("\t")[0]
                dIndex[sIdList] = f.tell()
        pickle.dump(dIndex, open(self.file.path +".pickle","wb"))

class ExpressionStudy(models.Model):

    article = models.CharField(max_length=200)
    pmid = models.CharField(max_length=20)
    ome = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    technology = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    species = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    experimental_design = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    topics = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    tissues = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    sex = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    dev_stage = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    age = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    antibody = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    mutant = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    cell_sorted = ArrayField(models.CharField(max_length=50, blank=True), default=list)
    keywords = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    samples_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_created_by')
    data = models.ManyToManyField(ExpressionData, related_name="studies")

    def __str__(self):
        return self.pmid
