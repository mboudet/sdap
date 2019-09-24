from django.urls import path
from sdap.files import views


app_name = 'files'
# Define urls here
urlpatterns = [
    path('', views.index, name='index'),
    path('create/file', views.create_file, name='create_file'),
    path('create/folder', views.create_folder, name='create_folder'),
    path('folder/<int:folderid>', views.subindex, name='subindex'),
    path('file/<int:fileid>', views.view_file, name='view_file'),
    path('file/<int:fileid>/visualize', views.get_visualization, name='get_visualization'),
    path('download/<int:fileid>', views.download_file, name='download_file'),
    path('ajax/file_filter', views.files_filter, name='file_filter'),


]
