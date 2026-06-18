from django.db import models


class Student(models.Model):
    name = models.CharField( max_length=50)
    gender = models.CharField(max_length=50)
    hours_studied = models.FloatField()
    attendance = models.FloatField()
    previous_score = models.IntegerField()
    marks = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

