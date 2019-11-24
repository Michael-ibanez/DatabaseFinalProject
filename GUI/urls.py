from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insertData', views.insertData, name='insertData'),
    path('queries', views.queries, name='queries'),
    path('extraCred', views.extraCred, name='extraCred'),
]
