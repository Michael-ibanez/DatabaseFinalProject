from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the main index. Here we will"
    + " have buttons that go to different functions <INLCUDE BUTTONS>")

def dataInput(request):
    return HttpResponse("Hello, world. You're at the main index. Here we will"
    + " have forms go to insert condtions, measurements, information about"
    + " sequences and experiments with its own conditions and results")

def dataInputCondition(request):
    return HttpResponse("Form to insert condition")

def dataInputMeasurement(request):
    return HttpResponse("Form to insert measurement")
    
def dataInputSequence(request):
    return HttpResponse("Form to insert sequence")

def dataInputExperiment(request):
    return HttpResponse("Form to insert experiment with conditions and results")

def insertCSV(request):
    return HttpResponse("Hello, world. You're at the insert test data from CSV"
    + " index. We need to take file and insert all of the data from it")

def queries(request):
    return HttpResponse("Hello, world. You're at the queries index. Here we will"
     + " have two forms that go to Experiment info and Side by side comparisons"
     + " of two experiments")

def queryExperiment(request):
    return HttpResponse("Form to query an experiment")

def querySideBySide(request):
    return HttpResponse("Form to query two experiments and compare")

def extraCred(request):
    return HttpResponse("Hello, world. You're at the extra credit index. Here we"
     + " will have two forms that go to enter list of sequences and conditions"
     + " or a list of measurements")

def extraCredPart1(request):
    return HttpResponse("Form to query sequences and conditions")

def extraCredPart2(request):
    return HttpResponse("Form to query list of measurements")
