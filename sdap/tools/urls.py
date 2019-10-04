from django.urls import path
from sdap.tools import views

app_name = 'tools'
# Define urls here
urlpatterns = [
    # ex: /tools/
    path('', views.IndexView.as_view(), name='index'),
    path('analyze', views.AnalyseIndexView.as_view(), name='analyze'),
    path('pipelines', views.IndexView.as_view(), name='pipelines'),
    path('visualization', views.IndexView.as_view(), name='visualization'),
    # ex: /tools/5/
    # the 'name' value as called by the {% url %} template tag
    path('<int:toolid>/', views.DetailView, name='detail'),
]
