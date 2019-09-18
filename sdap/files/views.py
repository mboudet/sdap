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
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from mimetypes import guess_type
from django.urls import reverse_lazy


from sdap.files.models import File
from celery.result import AsyncResult

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'files/index.html'
    context_object_name = 'files'

    # Restrict to user
    def get_queryset(self):
        return File.objects.filter(
            created_by= self.request.user
        ).order_by('-created_at')[:5]
