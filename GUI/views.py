from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from sqlescapy import sqlescape

from .models import Sequence, Measurement, Condition, SpecificCondition, SpecificMeasurement, Experiment


# Index page of our project
def index(request):
    context = {'someVariable': '0', }
    return render(request, 'GUI/index.html', context)


# Data input page of our project
def insertData(request):
    return render(request, 'GUI/insertData.html')


def dataQuery(request):
    cursor = connection.cursor()
    print("lol")
    return render(request, 'GUI/queries.html')


# Form for input Needs a condition(Name, domain, and possible values)
def dataInputCondition(request):
    cursor = connection.cursor()
    condName = 'none'
    condDomain = 'any'
    possibleValues = 'any'
    # Check if that condition already exists
    sql_search_query = ("SELECT * FROM GUI_Condition WHERE name=%s")
    condQuery = (condName,)
    cursor.execute(sql_search_query, condQuery)
    condFound = cursor.fetchall()
    if len(condFound) == 0:
        newCon = Condition(name=condName, domain=condDomain, possValues=possibleValues)
        newCon.save()
        print("Condition inserted successfully")
    else:
        print("Condition was already found. Try another Condition")
    return render(request, 'GUI/insertedComplete.html')


# Form for input Needs a measurement(Name, domain, and possible values)
def dataInputMeasurement(request):
    cursor = connection.cursor()
    measName = 'none'
    measDomain = 'any'
    possibleValues = 'any'
    # Check if that measurement already exists
    sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
    measQuery = (measName,)
    cursor.execute(sql_search_query, measQuery)
    measFound = cursor.fetchall()
    if len(measFound) == 0:
        newMeas = Condition(name=measName, domain=measDomain, possValues=possibleValues)
        newMeas.save()
        print("Measurement inserted successfully")
    else:
        print("Measurement was already found. Try another Measurment")
    return render(request, 'GUI/insertedComplete.html')


# Form for input Needs a sequence(Name and info)
def dataInputSequence(request):
    cursor = connection.cursor()
    seqName = 'none'
    seqInfo = 'none'
    # Check if that sequence already exists
    sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
    seqQuery = (seqName,)
    cursor.execute(sql_search_query, seqQuery)
    seqFound = cursor.fetchall()
    if len(seqFound) == 0:
        newSeq = Condition(name=seqName, info=seqInfo)
        newSeq.save()
        print("Sequence inserted successfully")
    else:
        print("Sequence was already found. Try another Sequence")
    return render(request, 'GUI/insertedComplete.html')


# Form for input Needs an experiment(Sequence name, conditions and measurements)
def dataInputExperiment(request):
    cursor = connection.cursor()
    seqName = 'none'
    condList = 'none'
    conds = []
    # Check if that sequence already exists
    sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
    seqQuery = (seqName,)
    cursor.execute(sql_search_query, seqQuery)
    seqFound = cursor.fetchall()
    if len(seqFound) > 0:
        # For each condition check if it exists
        for a in condList:
            print(a)
    else:
        print("No sequence found")

    return render(request, 'GUI/insertedComplete.html')


def invalidInsert(request):
    return render(request, 'GUI/invalidInsert.html')


# Form for inputting a csv file
def insertCSV(request):
    csv_file = request.FILES['csv_file']

    if csv_file.multiple_chunks():
        print("File is too big")

    # Read in each line of the csv file
    try:
        file_data = csv_file.read().decode("utf-8")
    except Exception:
        return render(request, 'GUI/invalidInsert.html')
    lines = file_data.split("\r\n")
    # Loop over the lines and save them in db. If error , store as string and then display
    # First line contains the experiments so read those in first as experiments
    lineOne = lines[0]
    fields = lineOne.split(",")
    seqCond = {}
    conds = []
    measurements = []
    count = 0
    curr = 0
    measurement = 0
    cursor = connection.cursor()
    # Each is a particular seq with its conditions
    for exp in fields:
        ## insert into db the sequence if it doesnt exist(line[0])
        line = exp.split("_")
        seqCond[count] = line[0]
        conds.append([])
        measurements.append([])
        sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
        seqQuery = (line[0],)
        cursor.execute(sql_search_query, seqQuery)
        sequenceFound = cursor.fetchall()
        if len(sequenceFound) == 0:
            newSeq = Sequence(name=line[0], info="Nothing")
            newSeq.save()
            print("Inserting ", line[0], " into the database as a sequence")
        else:
            print(line[0], " is already inserted into the database")
        # Insert into db the specific condition and if it doesnt exist store the id
        for i in range(1, len(line), 2):
            # Check if a condition exists with that name else insert it
            sql_search_query = ("SELECT * FROM GUI_Condition WHERE name=%s")
            ConQuery = (line[i],)
            cursor.execute(sql_search_query, ConQuery)
            conFound = cursor.fetchall()
            if len(conFound) == 0:
                newCon = Condition(name=line[i], domain="any", possValues="any")
                newCon.save()
            # Check if the specific condition exists else insert it
            sql_search_query = ("SELECT * FROM GUI_SpecificCondition WHERE name=%s AND value=%s")
            SpecConQuery = (line[i], line[i + 1],)
            cursor.execute(sql_search_query, SpecConQuery)
            SpecConFound = cursor.fetchall()
            if len(SpecConFound) == 0:
                newSpecCon = SpecificCondition(name=sqlescape(line[i]), value=sqlescape(line[i + 1]))
                newSpecCon.save()
                print("Added new specific condition : ", newSpecCon.id)
                conds[count].append(newSpecCon.id)
            else:
                print("Found previous specific condition: ", SpecConFound[0][0])
                conds[count].append(SpecConFound[0][0])
        count += 1
    # Each is a specific measurement
    for line in lines[1:-1]:
        fields = line.split(",")
        data_dict = {}
        data_dict['measurement'] = fields[0]
        print(data_dict['measurement'])
        curr = 0;
        # Check if a measurement exists with that name else insert it
        sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
        measurementQuery = (fields[0],)
        cursor.execute(sql_search_query, measurementQuery)
        measurementFound = cursor.fetchall()
        if len(measurementFound) == 0:
            newMeasurement = Measurement(name=sqlescape(fields[0]), domain="any", possValues="any")
            newMeasurement.save()

        # Insert into db the specific measurement and if it doesnt exist store the id
        for exp in fields[1:]:
            sql_search_query = ("SELECT * FROM GUI_SpecificMeasurement WHERE name=%s AND value=%s")
            SpecMeaQuery = (fields[0], exp,)
            cursor.execute(sql_search_query, SpecMeaQuery)
            SpecMeaFound = cursor.fetchall()
            if len(SpecMeaFound) == 0:
                newSpecMea = SpecificMeasurement(name=sqlescape(fields[0]), value=sqlescape(exp))
                newSpecMea.save()
                print("\tAdded new specific measurement : ", newSpecMea.id)
                measurements[curr].append(newSpecMea.id)
            else:
                print("\tFound previous specific measurement: ", SpecMeaFound[0][0])
                measurements[curr].append(SpecMeaFound[0][0])
            curr += 1
        while curr < count:
            print("\tSequence ", curr, " has var " + fields[0] + " of null")
            curr += 1
    # For each combo of sequences and conditions insert all of the measurements for that seqCond
    #   to make an experiment if it doesnt exist
    it = 0
    while it < count:
        conds[it].sort()
        print(seqCond[it], " has conditions:", str(conds[it]).strip('[]'), " and measurements:",
              str(measurements[it]).strip('[]'))
        sql_search_query = ("SELECT * FROM GUI_Experiment WHERE sequence=%s AND conditions=%s")
        SpecCond = str(conds[it]).strip('[]')
        SpecMeasure = str(measurements[it]).strip('[]')
        expQuery = (seqCond[it], SpecCond,)
        cursor.execute(sql_search_query, expQuery)
        expFound = cursor.fetchall()
        if len(expFound) == 0:
            newExp = Experiment(sequence=sqlescape(seqCond[it]), conditions=sqlescape(SpecCond), measurements=sqlescape(SpecMeasure))
            newExp.save()
            print("Experiment was inserted.")
        else:
            print("Experiment has already been recorded. Try another experiment")
        it += 1
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
