from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from sqlescapy import sqlescape

from .models import Sequence, Measurement, Condition, SpecificCondition, SpecificMeasurement, Experiment


# Index page of our project
def index(request):
    context = {'someVariable': '0', }
    return render(request, 'GUI/index.html', context)


def error(request):
    return render(request, 'GUI/error.html')


# Data input page of our project
def insertData(request):
    return render(request, 'GUI/insertData.html')


def results(request):
    return render(request, 'GUI/results.html')


#
# def dataQuery(request):
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             expConditions = ''
#             measureConditions = ''
#             seqName = request.POST.get('seqName')
#             if request.POST.get('expConditions') != '':
#                 expConditions = request.POST.get('expConditions')
#             if request.POST.get('measureConditions') != '':
#                 measureConditions = request.POST.get('measureConditions')
#             query = 'SELECT * FROM gui_sequence WHERE name = "{}"'.format(sqlescape(seqName))
#             cursor.execute(query)
#             condFound = cursor.fetchall()
#             context = {'found': False}
#             if len(condFound) > 0:
#                 context = {'allPosts': json.dumps(dict(condFound)), 'found': True}
#                 return render(request, 'GUI/results.html', context)
#             return render(request, 'GUI/results.html', context)


# Form for input Needs a condition(Name, domain, and possible values)
def dataInputCondition(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            condName = 'none'
            condDomain = 'any'
            possibleValues = 'any'
            # Check if that condition already exists
            sql_search_query = "SELECT * FROM GUI_Condition WHERE name=%s"
            condQuery = (condName,)
            cursor.execute(sql_search_query, condQuery)
            condFound = cursor.fetchall()
            if len(condFound) == 0:
                newCon = Condition(name=sqlescape(condName), domain=sqlescape(condDomain),
                                   possValues=sqlescape(possibleValues))
                newCon.save()
                print("Condition inserted successfully")
            else:
                print("Condition was already found. Try another Condition")
            return render(request, 'GUI/insertedComplete.html')


# Form for input Needs a measurement(Name, domain, and possible values)
def dataInputMeasurement(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            measName = 'none'
            measDomain = 'any'
            possibleValues = 'any'
            # Check if that measurement already exists
            sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
            measQuery = (measName,)
            cursor.execute(sql_search_query, measQuery)
            measFound = cursor.fetchall()
            if len(measFound) == 0:
                newMeas = Condition(name=sqlescape(measName), domain=sqlescape(measDomain),
                                    possValues=sqlescape(possibleValues))
                newMeas.save()
                print("Measurement inserted successfully")
            else:
                print("Measurement was already found. Try another Measurement")
            return render(request, 'GUI/insertedComplete.html')


# Form for input Needs a sequence(Name and info)
def dataInputSequence(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            seqName = 'none'
            seqInfo = 'none'
            # Check if that sequence already exists
            sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
            seqQuery = (seqName,)
            cursor.execute(sql_search_query, seqQuery)
            seqFound = cursor.fetchall()
            if len(seqFound) == 0:
                newSeq = Condition(name=sqlescape(seqName), info=sqlescape(seqInfo))
                newSeq.save()
                print("Sequence inserted successfully")
            else:
                print("Sequence was already found. Try another Sequence")
            return render(request, 'GUI/insertedComplete.html')


# Form for input Needs an experiment(Sequence name, conditions and measurements)
def dataInputExperiment(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
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
    if request.method == 'POST':
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
        with connection.cursor() as cursor:
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
                        newCon = Condition(name=sqlescape(line[i]), domain="any", possValues="any")
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
                    newExp = Experiment(sequence=sqlescape(seqCond[it]), conditions=sqlescape(SpecCond),
                                        measurements=sqlescape(SpecMeasure))
                    newExp.save()
                    print("Experiment was inserted.")
                else:
                    print("Experiment has already been recorded. Try another experiment")
                it += 1
            return render(request, 'GUI/insertedComplete.html')


# Query page of our project
def queries(request):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM GUI_Experiment'
        cursor.execute(query)
        expFound = cursor.fetchall()
        list = {}
        for exp in expFound:
            list[exp[0]] = exp[0]
        context = {'data':({"choices":list})}
        return render(request, 'GUI/queries.html',context)


# Form for query experiment(Sequence name and conditions)
def queryExperiment(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            expConditions = ''
            seqName = request.POST.get('seqName')
            if request.POST.get('expConditions') != '':
                expConditions = request.POST.get('expConditions')

            # Check all of the specific conditions and find the ids for them
            expConditions = ''.join(expConditions.split())
            listSpecCond = expConditions.split(',')
            list = []
            for specCondition in listSpecCond:
                item = specCondition.split(':')
                query = 'SELECT * FROM GUI_SpecificCondition WHERE name = "{}" AND value = "{}"'.format(
                    sqlescape(item[0]), sqlescape(item[1]))
                cursor.execute(query)
                condFound = cursor.fetchall()
                for a in condFound:
                    list.append(a[0])
            list.sort()
            newList = str(list).strip('[]')
            query = 'SELECT * FROM GUI_Experiment WHERE sequence = "{}" AND Conditions = "{}"'.format(
                sqlescape(seqName), sqlescape(newList))
            cursor.execute(query)
            expFound = cursor.fetchall()
            context = {'found': False}
            if len(expFound) > 0:
                se = request.POST.get('seqName')
                es = request.POST.get('expConditions')
                measurementList = {}
                myList = expFound[0][3].split(', ')
                for a in myList:
                    query = 'SELECT * FROM GUI_SpecificMeasurement WHERE id = "{}"'.format(sqlescape(a))
                    cursor.execute(query)
                    measurementFound = cursor.fetchall()
                    if len(measurementFound) > 0:
                        mesua = measurementFound[0]
                        measurementList[mesua[1]] = mesua[2]
                context = {"data": ({"ExperimentFound": expFound, "es": es, "se": se, "measurements": measurementList}),
                           "found": True}
                print(context)
                return render(request, 'GUI/results.html', context)
            return render(request, 'GUI/results.html', context)


# Form for query side by side comparison of two experiments
def querySideBySide(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            expConditions = ''
            seqName = request.POST.get('seqName')
            if request.POST.get('expConditions') != '':
                expConditions = request.POST.get('expConditions')

            # Check all of the specific conditions and find the ids for them
            expConditions = ''.join(expConditions.split())
            listSpecCond = expConditions.split(',')
            list = []
            for specCondition in listSpecCond:
                item = specCondition.split(':')
                query = 'SELECT * FROM GUI_SpecificCondition WHERE name = "{}" AND value = "{}"'.format(
                    sqlescape(item[0]), sqlescape(item[1]))
                cursor.execute(query)
                condFound = cursor.fetchall()
                for a in condFound:
                    list.append(a[0])
            list.sort()
            newList = str(list).strip('[]')
            query = 'SELECT * FROM GUI_Experiment WHERE sequence = "{}" AND Conditions = "{}"'.format(
                sqlescape(seqName), sqlescape(newList))
            cursor.execute(query)
            expFound = cursor.fetchall()
            context = {'found': False}
            if len(expFound) > 0:
                se = request.POST.get('seqName')
                es = request.POST.get('expConditions')
                measurementList = {}
                myList = expFound[0][3].split(', ')
                for a in myList:
                    query = 'SELECT * FROM GUI_SpecificMeasurement WHERE id = "{}"'.format(sqlescape(a))
                    cursor.execute(query)
                    measurementFound = cursor.fetchall()
                    if len(measurementFound) > 0:
                        mesua = measurementFound[0]
                        measurementList[mesua[1]] = mesua[2]
                context = {"data": ({"ExperimentFound": expFound, "es": es, "se": se, "measurements": measurementList}),
                           "found": True}
                print(context)
                return render(request, 'GUI/results.html', context)
            return render(request, 'GUI/results.html', context)


# Extra credit page of our project
def extraCred(request):
    return render(request, 'GUI/extraCred.html')


# Form for extra credit query
def queryExtraCred(request):
    #   The user should enter a list of sequences and conditions.
    #
    #       Then the system should retrieve all experiments that has the sequence and
    #           (at least) one of the conditions and list them.
    #
    #   The user can also enter a list of measurements and the system will return the value
    #       of the measurements for all the experiments above as a table.

    if request.method == 'POST':
        with connection.cursor() as cursor:
            seqName = request.POST.get('seqName')

            # list of experiment names
            expConditions = request.POST.get('expConditions')
            expConditions = ''.join(expConditions.split()).split(',')

            # list of measurement names
            expMeasures = request.POST.get('expMeasures')
            expMeasures = ''.join(expMeasures.split()).split(',')

            expFound = []

            query = 'SELECT * FROM GUI_Experiment e WHERE e.sequence = "{}"'.format(sqlescape(seqName))
            cursor.execute(query)
            for experiment in cursor.fetchall():
                # TODO: replace experiment.conditions with actual condition id list
                # expirement[1] is expected to be list of condition ids
                for condition_id in experiment[1]:

                    query = 'SELECT * FROM GUI_SpecificCondition sc WHERE sc.id = "{}" AND sc.name IN "{}"'.format(sqlescape(condition_id), sqlescape(expConditions))
                    cursor.execute(query)

                    if len(cursor.fetchall()) > 0:
                        if expMeasures != '':
                            # TODO: replace experiment.measurements with actual measurement id list
                            # expirement[2] expected to be list of measurement ids
                            query = 'SELECT sm.name, sm.value from GUI_SpecificMeasurement sm WHERE sm.id IN "{}" AND sm.name IN "{}"'.format(sqlescape(experiment[2]), sqlescape(expMeasures))
                            cursor.execute(query)

                            expFound.append((experiment, cursor.fetchall()))
                        else:
                            expFound.append(experiment)

                        break

            context = {'ExperimentsFound': expFound, 'found': len(expFound) > 0}
            return render(request, 'GUI/results.html', context)
