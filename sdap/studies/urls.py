from django.urls import path
from sdap.studies import views

app_name = 'studies'
# Define urls here
urlpatterns = [
    path('', views.index, name='index'),
    path('select/table', views.render_table, name='render_table'),
    path('select/document', views.document_select, name='select_documents'),
    path('graph', views.graph, name='graph'),
]
