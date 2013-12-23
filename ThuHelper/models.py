# coding=utf-8

# models.py
# 数据库model

from django.db import models

class Classroom(models.Model):
    building = models.CharField(max_length=10)
    floor = models.IntegerField()
    roomnumber = models.CharField(max_length=50)
    Monday = models.CharField(max_length=10)
    Tuesday = models.CharField(max_length=10)
    Wednesday = models.CharField(max_length=10)
    Thursday = models.CharField(max_length=10)
    Friday = models.CharField(max_length=10)
    Saturday = models.CharField(max_length=10)
    Sunday = models.CharField(max_length=10)

    def __unicode__(self):
        return self.roomnumber

class Onlinemusic(models.Model):
    imageURL = models.CharField(max_length=250)
    title = models.CharField(max_length=50)
    singer = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    type1 = models.CharField(max_length=10)
    type2 = models.CharField(max_length=10)
    type3 = models.CharField(max_length=10)

    def __unicode__(self):
        return self.title

class User(models.Model):
    openid = models.CharField(max_length=250)
    latestsignuptime = models.FloatField()
    signupstatus = models.CharField(max_length=50)
    sumtime = models.IntegerField()

    def __unicode__(self):
        return self.openid
