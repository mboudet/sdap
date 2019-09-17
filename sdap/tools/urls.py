from django.urls import path
from sdap.tools import views

app_name = 'tools'
# Define urls here
urlpatterns = [
    # ex: /tools/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /tools/5/
    # the 'name' value as called by the {% url %} template tag
    path('<int:toolid>/', views.DetailView, name='detail'),
]
