from django.db import models


### Each of these need to be inserted on their own(Listed by their names)
class Sequence(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    info = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Measurement(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    domain = models.CharField(max_length=128)
    possValues = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    domain = models.CharField(max_length=128)
    possValues = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


###

### Specific condition and measurements for each sequence (listed by their ids)
class SpecificCondition(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class SpecificMeasurement(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


###

### A combo of sequence and condition with a specific measurement(Listed by their ids)
class Experiment(models.Model):
    sequence = models.CharField(max_length=128)  # Name of sequence
    conditions = models.CharField(max_length=250)  # List of conditions sep by comma
    measurements = models.CharField(max_length=250)  # List of measurements sep by comma

    class Meta:
        unique_together = (("sequence", "conditions"),)

    def __unicode__(self):
        return self.sequence + " -> " + self.conditions + " & " + self.measurements
