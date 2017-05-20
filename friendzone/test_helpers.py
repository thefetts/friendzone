from django.test import TestCase
from django.utils.dateparse import parse_date


class TestHelpers(TestCase):
    def get_validation_errors(self, model, field):
        with self.assertRaises(Exception) as context:
            model.full_clean()
        return context.exception.message_dict[field]

    def get_date(self, date_string='2017-05-05'):
        return parse_date(date_string)
