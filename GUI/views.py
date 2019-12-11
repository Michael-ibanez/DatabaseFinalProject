from django.shortcuts import render
from django.http import HttpResponse

# Index page of our project
def index(request):
    context = {'someVariable': '0',}
    return render(request, 'GUI/index.html', context)
# Data input page of our project
def insertData(request):
    if request.method == 'POST':
        return insertCSV(request)
    else:
        return render(request, 'GUI/insertData.html')
# Form for input
def dataInputCondition(request):
    return render(request, 'GUI/insertedComplete.html')
# Form for input
def dataInputMeasurement(request):
    return render(request, 'GUI/insertedComplete.html')
# Form for input
def dataInputSequence(request):
    return render(request, 'GUI/insertedComplete.html')
# Form for input
def dataInputExperiment(request, data):
    return render(request, 'GUI/insertedComplete.html')
# Form for input
def insertCSV(request):
    csv_file = request.FILES['csv_file']

    if csv_file.multiple_chunks():
        print("File is too big")

    # Read in each line of the csv file
    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    # Loop over the lines and save them in db. If error , store as string and then display
    # First line contains the experiments so read those in first as experiments
    lineOne = lines[0]
    fields = lineOne.split(",")
    experiments = {}
    count = 0;
    curr = 0;
    for exp in fields:
        experiments[count] = exp
        print("Inserted "+ exp+ " into the database as a sequence")
        count+= 1
    print(experiments)
    for line in lines[1:-1]:
        fields = line.split(",")
        data_dict = {}
        data_dict['measurement'] = fields[0]
        curr = 0;
        for exp in fields[1:]:
            data_dict[count] = exp
            print("Sequence ", curr, " has var "+fields[0]+" of "+exp)
            curr += 1
        while curr < count:
            print("Sequence ",curr, " has var "+fields[0]+" of nothing")
            curr += 1

        print(data_dict)

        ###### What we use to insert
        """
        try:
            form = EventsForm(data_dict)
            if form.is_valid():
                form.save()
            else:
                logging.getLogger("error_logger").error(form.errors.as_json())
        except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass
        """
    return render(request, 'GUI/insertedComplete.html')

# Query page of our project
def queries(request):
    return render(request, 'GUI/queries.html')
# Form for query
def queryExperiment(request):
    return HttpResponse("Form to query an experiment")
# Form for query
def querySideBySide(request):
    return HttpResponse("Form to query two experiments and compare")
# Extra credit page of our prokect
def extraCred(request):
    return render(request, 'GUI/extraCred.html')
# Form for extra credit query
def extraCredPart1(request):
    return HttpResponse("Form to query sequences and conditions")
# Form for extra credit query
def extraCredPart2(request):
    return HttpResponse("Form to query list of measurements")
