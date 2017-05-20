import datetime

from django.db import models
from django.utils import timezone


class Friend(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Friendship(models.Model):
    friend1 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend2')
    met_date = models.DateTimeField('date met')

    def __str__(self):
        return self.friend1.name + ' and ' + self.friend2.name + ' on ' + str(self.met_date)

    def met_recently(self):
        return self.met_date >= timezone.now() - datetime.timedelta(days=30)
