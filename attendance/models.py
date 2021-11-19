from django.db import models
from account.models import MyUser
from datetime import datetime
from django.utils import timezone


class Grade(models.Model):
    id = models.BigAutoField(primary_key=True)
    grade = models.IntegerField(default=1)

    object = models.Manager()


class Class(models.Model):
    id = models.BigAutoField(primary_key=True)
    cls = models.IntegerField(default=1)

    objects = models.Manager()


class Period(models.Model):
    id = models.BigAutoField(primary_key=True)
    period = models.IntegerField(default=1)

    objects = models.Manager()


class Place(models.Model):
    id = models.BigAutoField(primary_key=True)
    grade = models.ForeignKey(Grade, default=None, on_delete=models.CASCADE)
    place = models.CharField(max_length=30, null=True)

    objects = models.Manager()


class AttendanceBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, default=None, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, default=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check = models.BooleanField(default=False)

    objects = models.Manager()

    def get_id(self):
        return self.id