from django.db import models

class classroom(models.Model):
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