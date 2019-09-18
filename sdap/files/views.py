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
