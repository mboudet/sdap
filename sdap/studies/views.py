import os
import json
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string

from django.views.generic import CreateView

import pandas as pd
import uuid
import shutil
from .models import ExpressionStudy, ExpressionData
from .forms import *

def index(request):

    columns = [
            "article",
            "pmid",
            "ome",
            "technology",
            "species",
            "experimental_design",
            "topics",
            "tissues",
            "sex",
            "dev_stage",
            "age",
            "antibody",
            "mutant",
            "cell_sorted",
            "keywords",
    ]

    studies = ExpressionStudy.objects.exclude(data=None)
    form = ExpressionStudyFilterForm(studies=studies)
    table = render_to_string('studies/partial_study_table.html', {'studies': studies}, request)
    context = {'form': form, 'columns': columns, 'table': table}
    return render(request, 'studies/scatter_plot.html', context)

def document_select(request):

    if not "id" in request.GET:
        return redirect(reverse("studies:index"))

    id_list = request.GET.getlist("id")
    # Just in case
    if not all(x.isdigit() for x in id_list):
        return redirect(reverse("studies:index"))

    studies = ExpressionStudy.objects.filter(id__in=id_list)
    if studies.count() == 0:
        return redirect(reverse("studies:index"))

    return render(request, 'studies/document_select.html', {'studies': studies})

def graph(request):

    if not "id" in request.GET:
        return redirect(reverse("studies:index"))

    id_list = request.GET.getlist("id")
    # Just in case
    if not all(x.isdigit() for x in id_list):
        return redirect(reverse("studies:index"))
    studies = ExpressionStudy.objects.filter(data__id__in=id_list)
    raise Exception(studies)


def render_table(request):

    data = {}
    studies = ExpressionStudy.objects.exclude(data=None)
    kwargs = {}
    for key, value in request.GET.items():
        if value:
            if key == "article":
                kwargs[key + "__icontains"] = [value]
            else:
                kwargs[key + "__contains"] = [value]

    studies = studies.filter(**kwargs)
    # Filter here
    table = render_to_string('studies/partial_study_table.html', {'studies': studies}, request)
    data['table'] = table
    return JsonResponse(data)
