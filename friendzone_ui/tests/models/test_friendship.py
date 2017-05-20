from django.test import TestCase
from django.utils import timezone

from friendzone.test_helpers import TestHelpers
from friendzone_ui.models.friend import Friend
from friendzone_ui.models.friendship import Friendship


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
        self.friendship = Friendship(friend1=self.fallon, friend2=self.hagan, met_date=self.helpers.get_date())

    def test_it_can_be_valid(self):
        self.assertEqual(self.friendship.full_clean(), None)

    def test_friend1_cannot_be_null(self):
        self.friendship.friend1 = None
        err = self.helpers.get_validation_errors(self.friendship, 'friend1')
        self.assertEqual(['This field cannot be null.'], err)

    def test_friend2_cannot_be_null(self):
        self.friendship.friend2 = None
        err = self.helpers.get_validation_errors(self.friendship, 'friend2')
        self.assertEqual(['This field cannot be null.'], err)

    def test_friend1_cannot_also_be_friend2(self):
        self.friendship.friend2 = self.friendship.friend1
        err = self.helpers.get_validation_errors(self.friendship, 'friend1')
        self.assertEqual(['Jordan Fallon cannot be both friends.'], err)

    def test_met_date_cannot_be_null(self):
        self.friendship.met_date = None
        err = self.helpers.get_validation_errors(self.friendship, 'met_date')
        self.assertEqual(['This field cannot be null.'], err)

    def test_met_date_is_not_in_the_future(self):
        self.friendship.met_date = self.helpers.get_date('3000-05-05')
        err = self.helpers.get_validation_errors(self.friendship, 'met_date')
        self.assertEqual(['Date cannot be in the future.'], err)

    def test_met_date_can_be_today(self):
        self.friendship.met_date = timezone.now().date()
        self.assertEqual(self.friendship.full_clean(), None)

    def test_friendship_is_unique(self):
        Friendship(friend1=self.fallon, friend2=self.hagan, met_date=self.helpers.get_date()).save()
        err = self.helpers.get_validation_errors(self.friendship, 'friend1')
        self.assertEqual(['Jordan Fallon and Jordan Hagan are already friends.'], err)

    def test_friendship_is_unique_when_reversed(self):
        Friendship(friend1=self.hagan, friend2=self.fallon, met_date=self.helpers.get_date()).save()
        err = self.helpers.get_validation_errors(self.friendship, 'friend1')
        self.assertEqual(['Jordan Fallon and Jordan Hagan are already friends.'], err)

    def test_friendship_is_unique_on_update(self):
        self.friendship.save()
        self.assertIsNone(self.friendship.full_clean())
