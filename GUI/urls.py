from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insertCSV', views.dataInput, name='dataInput'),
    path('queries', views.queries, name='queries'),
]
