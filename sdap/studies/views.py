import os
import json
from datetime import datetime

from dal import autocomplete
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
from .models import ExpressionStudy, ExpressionData, Gene
from .forms import *
from .graphs import getClasses, get_graph_data_full, get_graph_data_genes

class GeneAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_value(self, result):
        return result.id

    def get_result_label(self, result):
        return result.symbol

    def get_queryset(self):
        query = self.q
        qs = Gene.objects.all()
        if query:
            qs = qs.filter(Q(symbol__icontains=query) | Q(synonyms__icontains=query)| Q(gene_id__icontains=query))
        return qs

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

def show_graph(request):

    if not "document_id" in request.GET and not "study_id" in request.GET:
        return redirect(reverse("studies:index"))

    document_id = request.GET["document_id"]
    study_id = request.GET["study_id"]
    # Just in case
    if not document_id.isdigit() or not study_id.isdigit():
        return redirect(reverse("studies:index"))

    document = get_object_or_404(ExpressionData, id=document_id)
    study = get_object_or_404(ExpressionStudy, id=study_id)
    classes = getClasses(document)
    context = {'study': study, 'document': document, 'classes': classes}
    return render(request, 'studies/graph.html', context)

def get_graph_data(request):
    
    if not "document_id" in request.GET:
        return redirect(reverse("studies:index"))

    document_id = request.GET["document_id"]

    if not document_id.isdigit():
        return redirect(reverse("studies:index"))

    data = get_object_or_404(ExpressionData, id=document_id)

    selected_class = request.GET.get('selected_class', None)

    if "gene_id" in request.GET:
        data = get_graph_data_genes(data, selected_class, request.GET['gene_id'])
    else:
        data = get_graph_data_full(data, selected_class)
    return JsonResponse(data)

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
