from django.db import connection
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
            condName = request.POST.get('name')
            condDomain = request.POST.get('domain')
            possibleValues = request.POST.get('possValues')
            # Check if that condition already exists
            sql_search_query = "SELECT * FROM GUI_Condition WHERE name=%s"
            condQuery = (sqlescape(condName),)
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
            measName = request.POST.get('name')
            measDomain = request.POST.get('domain')
            possibleValues = request.POST.get('possValues')
            # Check if that measurement already exists
            sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
            measQuery = (sqlescape(measName),)
            cursor.execute(sql_search_query, measQuery)
            measFound = cursor.fetchall()
            if len(measFound) == 0:
                newMeas = Measurement(name=sqlescape(measName), domain=sqlescape(measDomain),
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
            seqName = request.POST.get('name')
            seqInfo = request.POST.get('info')
            # Check if that sequence already exists
            sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
            seqQuery = (sqlescape(seqName),)
            cursor.execute(sql_search_query, seqQuery)
            seqFound = cursor.fetchall()
            if len(seqFound) == 0:
                newSeq = Sequence(name=sqlescape(seqName), info=sqlescape(seqInfo))
                newSeq.save()
                print("Sequence inserted successfully")
            else:
                print("Sequence was already found. Try another Sequence")
            return render(request, 'GUI/insertedComplete.html')


# Form for input Needs an experiment(Sequence name, conditions and measurements)

def dataInputExperiment(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            seqName = request.POST.get('name')
            condList = request.POST.get('conditions')
            measList = request.POST.get('measurements')
            conditionsList = []
            measurementsList = []
            # Check if that sequence already exists
            sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
            seqQuery = (sqlescape(seqName),)
            cursor.execute(sql_search_query, seqQuery)
            seqFound = cursor.fetchall()
            if len(seqFound) > 0:
                # For each condition check if it exists
                conList = condList.split(', ')
                flag = 1
                for a in conList:
                    aa = a.split(':')
                    sql_search_query = ("SELECT * FROM GUI_Condition WHERE name=%s")
                    seqQuery = (sqlescape(aa[0]),)
                    cursor.execute(sql_search_query, seqQuery)
                    conFound = cursor.fetchall()
                    if len(seqFound) == 0:
                        flag = 0
                if flag:
                    meaList = measList.split(', ')
                    flag2 = 1
                    for b in meaList:
                        bb = b.split(':')
                        sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
                        seqQuery = (sqlescape(bb[0]),)
                        cursor.execute(sql_search_query, seqQuery)
                        meaFound = cursor.fetchall()
                        if len(meaFound) == 0:
                            flag2 = 0;
                if flag2:
                    # insert all conditions and measurements then insert the experiment
                    for a in conList:
                        aa = a.split(':')
                        newSpecCon = SpecificCondition(name=sqlescape(aa[0]), value=sqlescape(aa[1]))
                        newSpecCon.save()
                        conditionsList.append(newSpecCon.id)
                    for b in meaList:
                        bb = b.split(':')
                        newSpecMea = SpecificCondition(name=sqlescape(bb[0]), value=sqlescape(bb[1]))
                        newSpecMea.save()
                        measurementsList.append(newSpecMea.id)
                    SpecCond = str(conditionsList).strip('[]')
                    SpecMeau = str(measurementsList).strip('[]')
                    newExp = Experiment(sequence=sqlescape(seqName), conditions=sqlescape(SpecCond),
                                        measurements=sqlescape(SpecMeau))
                    newExp.save()
            else:
                print("No sequence found")
                return error(request)
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
        with connection.cursor() as cursor:
            # Each is a particular seq with its conditions
            for exp in fields:
                # insert into db the sequence if it doesnt exist(line[0])
                line = exp.split("_")
                seqCond[count] = line[0]
                conds.append([])
                measurements.append([])
                sql_search_query = ("SELECT * FROM GUI_Sequence WHERE name=%s")
                seqQuery = (sqlescape(line[0]),)
                cursor.execute(sql_search_query, seqQuery)
                sequenceFound = cursor.fetchall()
                if len(sequenceFound) == 0:
                    newSeq = Sequence(name=sqlescape(line[0]), info="Nothing")
                    newSeq.save()
                    print("Inserting ", line[0], " into the database as a sequence")
                else:
                    print(line[0], " is already inserted into the database")
                # Insert into db the specific condition and if it doesnt exist store the id
                for i in range(1, len(line), 2):
                    # Check if a condition exists with that name else insert it
                    sql_search_query = ("SELECT * FROM GUI_Condition WHERE name=%s")
                    ConQuery = (sqlescape(line[i]),)
                    cursor.execute(sql_search_query, ConQuery)
                    conFound = cursor.fetchall()
                    if len(conFound) == 0:
                        newCon = Condition(name=sqlescape(line[i]), domain="any", possValues="any")
                        newCon.save()
                    # Check if the specific condition exists else insert it
                    sql_search_query = ("SELECT * FROM GUI_SpecificCondition WHERE name=%s AND value=%s")
                    SpecConQuery = (sqlescape(line[i]), sqlescape(line[i + 1]),)
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
                data_dict = {'measurement': fields[0]}
                print(data_dict['measurement'])
                curr = 0
                # Check if a measurement exists with that name else insert it
                sql_search_query = ("SELECT * FROM GUI_Measurement WHERE name=%s")
                measurementQuery = (sqlescape(fields[0]),)
                cursor.execute(sql_search_query, measurementQuery)
                measurementFound = cursor.fetchall()
                if len(measurementFound) == 0:
                    newMeasurement = Measurement(name=sqlescape(fields[0]), domain="any", possValues="any")
                    newMeasurement.save()

                # Insert into db the specific measurement and if it doesnt exist store the id
                for exp in fields[1:]:
                    sql_search_query = ("SELECT * FROM GUI_SpecificMeasurement WHERE name=%s AND value=%s")
                    SpecMeaQuery = (sqlescape(fields[0]), sqlescape(exp),)
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
                expQuery = (sqlescape(seqCond[it]), sqlescape(SpecCond),)
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
        dataList = []
        for exp in expFound:
            dataList.append(str(exp[0]) + " " + str(exp[1]) + " conditon ids: "+ str(exp[2]))
        context = {'data': ({"choices": dataList})}
        return render(request, 'GUI/queries.html', context)


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
            dataList = []
            for specCondition in listSpecCond:
                item = specCondition.split(':')
                query = 'SELECT * FROM GUI_SpecificCondition WHERE name = "{}" AND value = "{}"'.format(
                    sqlescape(item[0]), sqlescape(item[1]))
                cursor.execute(query)
                condFound = cursor.fetchall()
                for a in condFound:
                    dataList.append(a[0])
            dataList.sort()
            newList = str(dataList).strip('[]')
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
                           "found": True, "compare": False}
                return render(request, 'GUI/results.html', context)
            return render(request, 'GUI/results.html', context)


# Form for query side by side comparison of two experiments
def querySideBySide(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            one = request.POST.get('itemOneChoice')
            two = request.POST.get('itemTwoChoice')
            se1 = ''
            se2 = ''
            # Get both experiments and convert their measurementlists into list of ints
            query = 'SELECT * FROM GUI_Experiment WHERE id = "{}" '.format(
                sqlescape(one))
            cursor.execute(query)
            expOneFound = cursor.fetchall()
            for a in expOneFound[0][2]:
                query = 'SELECT * FROM GUI_SpecificCondition WHERE id = "{}" '.format(sqlescape(a))
                cursor.execute(query)
                s = cursor.fetchall()
                if len(s) > 0:
                    se1 +=s[0][1] + ':' + s[0][2] + ' '
            query = 'SELECT * FROM GUI_Experiment WHERE id = "{}" '.format(
                sqlescape(two))
            cursor.execute(query)
            expTwoFound = cursor.fetchall()
            for a in expTwoFound[0][2]:
                query = 'SELECT * FROM GUI_SpecificCondition WHERE id = "{}" '.format(sqlescape(a))
                cursor.execute(query)
                s = cursor.fetchall()
                if len(s) > 0:
                    se2 += s[0][1] + ':' + s[0][2] + ' '
            one = [int(i) for i in expOneFound[0][3].split(',')]
            two = [int(i) for i in expTwoFound[0][3].split(',')]
            one = set(one)
            two = set(two)
            es1 = expOneFound[0][1]
            es2 = expTwoFound[0][1]
            similarSet = one & two
            measurementList = {}
            for a in similarSet:
                query = 'SELECT * FROM GUI_SpecificMeasurement WHERE id = "{}"'.format(sqlescape(str(a)))
                cursor.execute(query)
                measurementFound = cursor.fetchall()
                if len(measurementFound) > 0:
                    mesua = measurementFound[0]
                    measurementList[mesua[1]] = mesua[2]
            context = {"data": ({"es1": es1, "es2": es2,"se1":se1,"se2":se2, "measurements": measurementList}),
                       "found": True, "compare": True}
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
            if expConditions != '':
                expConditions = ''.join(expConditions.split()).split(',')

            # list of measurement names
            expMeasures = request.POST.get('expMeasure')
            if expMeasures != '':
                expMeasures = ''.join(expMeasures.split()).split(',')

            expFound = []

            query = 'SELECT * FROM GUI_Experiment e WHERE e.sequence = "{}"'.format(sqlescape(seqName))
            cursor.execute(query)
            for experiment in cursor.fetchall():
                # TODO: replace experiment.conditions with actual condition id list
                # expirement[1] is expected to be list of condition ids
                for condition_id in experiment[1]:

                    query = 'SELECT * FROM GUI_SpecificCondition sc WHERE sc.id = "{}" AND sc.name IN "{}"'.format(
                        sqlescape(condition_id), sqlescape(expConditions))
                    cursor.execute(query)

                    if len(cursor.fetchall()) > 0:
                        if expMeasures != '':
                            # TODO: replace experiment.measurements with actual measurement id list
                            # expirement[2] expected to be list of measurement ids
                            query = 'SELECT sm.name, sm.value from GUI_SpecificMeasurement sm WHERE sm.id IN "{}" AND sm.name IN "{}"'.format(
                                sqlescape(experiment[2]), sqlescape(expMeasures))
                            cursor.execute(query)

                            expFound.append((experiment, cursor.fetchall()))
                        else:
                            expFound.append(experiment)

                        break

            context = {'ExperimentsFound': expFound, 'found': len(expFound) > 0}
            return render(request, 'GUI/results.html', context)
