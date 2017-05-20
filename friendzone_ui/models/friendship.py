import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .friend import Friend


class Friendship(models.Model):
    friend1 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='friend2')
    met_date = models.DateField('date met')
    conduit = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='conduit', null=True, blank=True)

    def __str__(self):
        return self.friend1.name + ' met ' + self.friend2.name + ' on ' + self.met_date.strftime('%B %d, %Y')

    def met_recently(self):
        return self.met_date >= timezone.now() - datetime.timedelta(days=30)

    def clean(self, *args, **kwargs):
        self.errors = {}
        self.met_date_cannot_be_in_the_future()

        if self.friends_are_set():
            self.friend1_is_not_friend2()
            self.friendship_is_unique()

            if self.conduit_id:
                self.neither_friend_is_conduit()
                self.conduit_is_mutual_friend()

        if len(self.errors):
            raise ValidationError(self.errors)

    def friend1_is_not_friend2(self):
        if self.friend1 == self.friend2:
            self.add_error('friend1', f'{self.friend1} cannot be both friends.')

    def met_date_cannot_be_in_the_future(self):
        if self.met_date is not None:
            if self.met_date > timezone.now().date():
                self.add_error('met_date', 'Date cannot be in the future.')

    def friendship_is_unique(self):
        same_friendships = Friendship.objects.exclude(pk=self.pk) \
            .filter(Q(friend1=self.friend1, friend2=self.friend2) | Q(friend1=self.friend2, friend2=self.friend1))
        if len(same_friendships) > 0:
            self.add_error('friend1', f'{self.friend1} and {self.friend2} are already friends.')

    def neither_friend_is_conduit(self):
        if self.friend1 == self.conduit:
            self.add_error('friend1', 'Friend1 cannot also be conduit.')
        if self.friend2 == self.conduit:
            self.add_error('friend2', 'Friend2 cannot also be conduit.')

    def conduit_is_mutual_friend(self):
        if self.friend1 != self.conduit and self.friend2 != self.conduit:
            if not len(Friendship.objects.all().filter(
                            Q(friend1=self.friend1, friend2=self.conduit) |
                            Q(friend1=self.conduit, friend2=self.friend1))):
                self.add_error('friend1', f'{self.friend1} and {self.conduit} are not friends.')
            if not len(Friendship.objects.all().filter(
                            Q(friend1=self.friend2, friend2=self.conduit) |
                            Q(friend1=self.conduit, friend2=self.friend2))):
                self.add_error('friend2', f'{self.friend2} and {self.conduit} are not friends.')

    def friends_are_set(self):
        return self.friend1_id and self.friend2_id

    def add_error(self, field, msg):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(msg)
