from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect

from sdap.files.models import File
from sdap.jobs.models import Job

def HomeView(request):
    if request.user.is_authenticated :
        user_files = File.objects.filter(created_by=request.user.id)
        user_jobs = Job.objects.filter(created_by=request.user.id)
        context = {'files':user_files, 'jobs':user_jobs}
        return render(request, 'pages/home.html',context)
    else:
            return HttpResponseRedirect(reverse('account_login'))