from django.shortcuts import render
from django.http import HttpResponse

# Index page of our project
def index(request):
    context = {'someVariable': '0',}
    return render(request, 'GUI/index.html', context)
# Data input page of our project
def dataInput(request):
    return render(request, 'GUI/insertData.html')
# Form for input
def dataInputCondition(request):
    return HttpResponse("Form to insert condition")
# Form for input
def dataInputMeasurement(request):
    return HttpResponse("Form to insert measurement")
# Form for input
def dataInputSequence(request):
    return HttpResponse("Form to insert sequence")
# Form for input
def dataInputExperiment(request):
    return HttpResponse("Form to insert experiment with conditions and results")
# Form for input
def insertCSV(request):
    return HttpResponse("Form to insert file and read in all of the data from it")
# Query page of our project
def queries(request):
    return HttpResponse("Hello, world. You're at the queries index. Here we will"
     + " have two forms that go to Experiment info and Side by side comparisons"
     + " of two experiments")
# Form for query
def queryExperiment(request):
    return HttpResponse("Form to query an experiment")
# Form for query
def querySideBySide(request):
    return HttpResponse("Form to query two experiments and compare")
# Extra credit page of our prokect
def extraCred(request):
    return HttpResponse("Hello, world. You're at the extra credit index. Here we"
     + " will have two forms that go to enter list of sequences and conditions"
     + " or a list of measurements")
# Form for extra credit query
def extraCredPart1(request):
    return HttpResponse("Form to query sequences and conditions")
# Form for extra credit query
def extraCredPart2(request):
    return HttpResponse("Form to query list of measurements")
