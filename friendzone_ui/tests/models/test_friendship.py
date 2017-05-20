from django.test import TestCase

from friendzone.test_helpers import TestHelpers
from friendzone_ui.models import Friend, Friendship


class FriendshipMethodsTest(TestCase):
    def setUp(self):
        self.helpers = TestHelpers()
        self.fallon = Friend(name='Jordan Fallon')
        self.hagan = Friend(name='Jordan Hagan')

    def test_str(self):
        friendship = Friendship(friend1=self.fallon, friend2=self.hagan, met_date=self.helpers.get_date())
        self.assertEqual(str(friendship), 'Jordan Fallon met Jordan Hagan on May 05, 2017')


class FriendshipValidationsTest(TestCase):
    def setUp(self):
        self.helpers = TestHelpers()
        self.fallon = Friend(name='Jordan Fallon')
        self.fallon.save()
        self.hagan = Friend(name='Jordan Hagan')
        self.hagan.save()

    def test_it_can_be_valid(self):
        friendship = Friendship(friend1=self.fallon, friend2=self.hagan, met_date=self.helpers.get_date())
        self.assertEqual(friendship.full_clean(), None)

    def test_friend1_cannot_be_null(self):
        friendship = Friendship(friend2=self.hagan, met_date=self.helpers.get_date())
        err = self.helpers.get_validation_errors(friendship, 'friend1')
        self.assertEqual(['This field cannot be null.'], err)

    def test_friend2_cannot_be_null(self):
        friendship = Friendship(friend1=self.fallon, met_date=self.helpers.get_date())
        err = self.helpers.get_validation_errors(friendship, 'friend2')
        self.assertEqual(['This field cannot be null.'], err)

    def test_friend1_cannot_also_be_friend2(self):
        friendship = Friendship(friend1=self.fallon, friend2=self.fallon, met_date=self.helpers.get_date())
        err = self.helpers.get_validation_errors(friendship, 'friend1')
        self.assertEqual(['Jordan Fallon cannot be both friends.'], err)
