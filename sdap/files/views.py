import os
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from mimetypes import guess_type
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from django.template.loader import render_to_string
from django.http import JsonResponse

import pandas as pd

from sdap.files.models import File, Folder

# Create your views here.
def index(request):

    folders = Folder.objects.filter(
            created_by= request.user,
            folder=None
       ).order_by('-created_at')

    files = File.objects.filter(
            created_by= request.user,
            folder=None
        ).order_by('-created_at')

    context = {'folders': folders, 'files': files}

    return render(request, 'files/index.html', context)


def subindex(request, folderid):


    previous_folder = Folder.objects.filter(
            created_by= request.user,
            folders=folderid
       )

    if previous_folder:
        back_url = reverse('files:subindex', kwargs={'folderid': previous_folder[0].id})
    else:
        back_url = reverse('files:index')

    folders = Folder.objects.filter(
            created_by= request.user,
            folder=folderid
       ).order_by('-created_at')

    files = File.objects.filter(
            created_by= request.user,
            folder=folderid
        ).order_by('-created_at')

    context = {'folders': folders, 'files': files, 'back_url': back_url}

    return render(request, 'files/index.html', context)

def view_file(request, fileid):

    # Check perm
    file = get_object_or_404(File, id=fileid)

    if not has_permission(request.user, file):
        return redirect('403/')
    # Need to make a list of available visualization tools based on type
    v_types = {
        'TEXT': ['Raw'],
        'IMAGE': ['Raw'],
        'CSV': ['Table', 'Pieplot', 'Barplot']
    }
    context = {'types': v_types[file.type], 'file': file}
    return render(request, 'files/visualize.html', context)


def get_visualization_parameters(request, fileid):

    file = get_object_or_404(File, id=fileid)
    if not has_permission(request.user, file):
        return redirect('403/')
    visu_type = request.GET.get('type', '')
    if not visu_type:
        return redirect('403/')

    data = {}
    if file.type == "CSV":
        # What if it's not tab separated?
        # Check file existence
        df = pd.read_csv(file.file, sep=",")
        df_head = df.head()
        table_content = df_head.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"])
        data['html'] = table_content
    return JsonResponse(data)

def visualize(request, file_id, vizualization_type):

    file = get_object_or_404(File, id=file_id)
    if not has_permission(request.user, file):
        return redirect('403/')

    if request.method == 'POST':
        if form.is_valid():
            "bla"
        else:
            data['form_is_valid'] = False
    else:
        form = "bla"


    context = {}
    return render(request, 'files/vizualize.html', context)



def has_permission(user,file):
    # TODO: Manage group permissions here
    has_permission = False
    if file.created_by == user:
        has_permission = True

    return has_permission

def download_file(request, fileid):
    file_object = get_object_or_404(File, pk=fileid)
    owner = file_object.created_by

    if owner != request.user :
        return HttpResponseForbidden()
    else :
        filename = file_object.file.name.split('/')[-1]
        response = HttpResponse(file_object.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
