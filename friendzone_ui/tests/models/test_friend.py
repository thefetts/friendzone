from django.test import TestCase

from friendzone.test_helpers import TestHelpers
from friendzone_ui.models import Friend


class FriendMethodsTest(TestCase):
    def test_str(self):
        friend = Friend(name='Jordan Hagan')
        self.assertEqual(str(friend), 'Jordan Hagan')


class FriendValidationsTest(TestCase):
    def setUp(self):
        self.helpers = TestHelpers()

    def test_name_cannot_be_null(self):
        friend = Friend()
        err = self.helpers.get_validation_errors(friend, 'name')
        self.assertEqual(['This field cannot be blank.'], err)

    def test_name_cannot_be_over_200_characters(self):
        friend = Friend(name='01234567890123456789012345678901234567890123456789012345678901234567890123456789'
                             '01234567890123456789012345678901234567890123456789012345678901234567890123456789'
                             '0123456789012345678901234567890123456789abcd')
        err = self.helpers.get_validation_errors(friend, 'name')
        self.assertEqual(['Ensure this value has at most 200 characters (it has 204).'], err)

    def test_name_must_be_unique(self):
        existing = Friend(name='Jordan Hagan')
        existing.save()

        friend = Friend(name='Jordan Hagan')
        err = self.helpers.get_validation_errors(friend, 'name')
        self.assertEqual(['Friend with this Name already exists.'], err)
