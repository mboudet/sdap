from django.urls import path
from sdap.files import views


app_name = 'files'
# Define urls here
urlpatterns = [
    path('', views.index, name='index'),
    path('folder/<int:folderid>', views.subindex, name='subindex'),
]
