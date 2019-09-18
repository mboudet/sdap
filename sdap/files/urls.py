from django.urls import path
from sdap.files import views


app_name = 'files'
# Define urls here
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
