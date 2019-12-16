from django.urls import path

from . import views

app_name = 'GUI'

urlpatterns = [
    path('', views.index, name='index'),
    path('insertData', views.insertData, name='insertData'),
    path('insertCSV', views.insertCSV, name='insertCSV'),
    path('dataInputCondition', views.dataInputCondition, name='dataInputCondition'),
    path('dataInputMeasurement', views.dataInputMeasurement, name='dataInputMeasurement'),
    path('dataInputSequence', views.dataInputSequence, name='dataInputSequence'),
    path('dataInputExperiment', views.dataInputExperiment, name='dataInputExperiment'),
    path('invalidInsert', views.invalidInsert, name='invalidInsert'),
    path('updated', views.updated, name='updated'),
    path('error', views.error, name='error'),
    path('presentation', views.presentation, name='presentation'),

    path('queries', views.queries, name='queries'),
    path('queryExperiment', views.queryExperiment, name='queryExperiment'),
    path('querySideBySide', views.querySideBySide, name='querySideBySide'),

    path('extraCred', views.extraCred, name='extraCred'),
    path('queryExtraCred', views.queryExtraCred, name='queryExtraCred'),

]
