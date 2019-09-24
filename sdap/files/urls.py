from django.urls import path
from sdap.files import views


app_name = 'files'
# Define urls here
urlpatterns = [
    path('', views.index, name='index'),
    path('create/file', views.create_file, name='create_file'),
    path('create/folder', views.create_folder, name='create_folder'),
    path('delete/file/<int:fileid>', views.delete_file, name='delete_file'),
    path('delete/folder/<int:folderid>', views.delete_folder, name='delete_folder'),
    path('folder/<int:folderid>', views.subindex, name='subindex'),
    path('file/<int:fileid>', views.view_file, name='view_file'),
    path('file/<int:fileid>/visualize', views.get_visualization, name='get_visualization'),
    path('download/<int:fileid>', views.download_file, name='download_file'),
    path('filter/<str:filter_by>/<int:fileid>', views.filter_files, name='filter_files'),

]
