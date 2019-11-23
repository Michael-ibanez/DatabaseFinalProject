from django.db import models

class Sequence(models.Model):
    name = models.CharField(max_length=128, unique=True)
    info = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Measurement(models.Model):
    name = models.CharField(max_length=128, unique=True)
    domain = models.CharField(max_length=128)
    possValues = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=128, unique=True)
    domain = models.CharField(max_length=128)
    possValues = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class SpecificCondition(models.Model):
    name = models.ForeignKey(Condition, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)

class SpecificMeasurement(models.Model):
    name = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)

class Experiment(models.Model):
    sequence = models.CharField(max_length=128)
    conditions = models.CharField(max_length=250)
    measurements = models.CharField(max_length=250)

    def __unicode__(self):
        return self.sequence + " -> " + self.conditions + " & " + self.measurements
