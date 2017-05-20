import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Friend(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Friendship(models.Model):
    friend1 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend2')
    met_date = models.DateField('date met')

    def __str__(self):
        return self.friend1.name + ' met ' + self.friend2.name + ' on ' + self.met_date.strftime('%B %d, %Y')

    def met_recently(self):
        return self.met_date >= timezone.now() - datetime.timedelta(days=30)

    def clean_fields(self, *args, **kwargs):
        super(Friendship, self).clean_fields(*args, **kwargs)
        self.friend1_is_not_friend2()

    def friend1_is_not_friend2(self):
        if self.friend1 == self.friend2:
            raise ValidationError({'friend1': [f'{self.friend1} cannot be both friends.']})
