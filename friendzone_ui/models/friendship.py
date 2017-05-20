import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .friend import Friend


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
        self.met_date_cannot_be_in_the_future()
        self.friendship_is_unique()

    def friend1_is_not_friend2(self):
        if self.friend1 == self.friend2:
            raise ValidationError({'friend1': [f'{self.friend1} cannot be both friends.']})

    def met_date_cannot_be_in_the_future(self):
        if self.met_date > timezone.now().date():
            raise ValidationError({'met_date': ['Date cannot be in the future.']})

    def friendship_is_unique(self):
        same_friendships = Friendship.objects.filter(friend1=self.friend1, friend2=self.friend2)
        reverse_friendships = Friendship.objects.filter(friend1=self.friend2, friend2=self.friend1)
        if len(same_friendships) + len(reverse_friendships) > 0:
            raise ValidationError({'friend1': [f'{self.friend1} and {self.friend2} are already friends.']})
