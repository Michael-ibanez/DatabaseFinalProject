from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insertCSV', views.insertCSV, name='insertCSV'),
    path('queries', views.queries, name='queries'),
]
