# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
import logging
import os
import sys

from unittest2 import TestCase

from ..eurovision import (
    add_countries_to_people,
    get_countries_from_csv,
    is_there_duplicate_countries,
    write_data_to_csv,
)


from ..person import Person


class TestEuroVision(TestCase):

    def setUp(self):
        self.countries = ['Ireland']
        self.people = [Person('Mike', self.countries)]

    def test_get_countries_from_csv_invalid_path(self):
        with self.assertRaises(OSError):
            get_countries_from_csv('some/made/up/path.csv')

    def test_get_countries_from_csv(self):
        countries = get_countries_from_csv(
            'eurovision/tests/csv/countries.csv'
        )

        # Some python version hackery
        if sys.version_info < (3, 0):
            expected = ['Ireland', 'Sweden', 'C__te_d___Ivoire']
        else:
            expected = ['Ireland', 'Sweden', 'C_te_d_Ivoire']

        self.assertEqual(countries, expected)

    def test_add_countries_to_people(self):
        ret_val = add_countries_to_people(
            self.people,
            self.countries,
            loop_count=1
        )
        person = ret_val[0]
        self.assertEqual(person.name, 'Mike')
        self.assertEqual(person.countries_dict['Ireland'], 1)

    def test_add_countries_to_people_no_endless_loop(self):
        people = [Person('Mike', self.countries, self.countries)]
        with self.assertRaises(RuntimeError):
            add_countries_to_people(people, self.countries, loop_count=1)

    def test_write_data_to_csv(self):
        write_data_to_csv('test.csv', self.people, self.countries)
        with open('test.csv', 'r') as test_csv:
            csv_data = test_csv.read()
            self.assertTrue('name,Ireland' in csv_data)
            self.assertTrue('Mike,0' in csv_data)
        os.remove('test.csv')

    def test_is_there_duplicate_countries_is_true(self):
        mike = Person('Mike', self.countries)
        mike.countries_dict['Ireland'] = 1

        eugene = Person('Eugene', self.countries)
        eugene.countries_dict['Ireland'] = 1

        country, maximum = mike.get_country_and_maximum_assignments()
        self.assertEqual(country, 'Ireland')
        self.assertEqual(maximum, 1)

        country, maximum = eugene.get_country_and_maximum_assignments()
        self.assertEqual(country, 'Ireland')
        self.assertEqual(maximum, 1)

        ret_val = is_there_duplicate_countries([mike, eugene])
        self.assertTrue(ret_val)

    def test_is_there_duplicate_countries_is_false(self):
        mike = Person('Mike', self.countries + ['Croatia'])
        mike.countries_dict['Croatia'] = 1

        eugene = Person('Eugene', self.countries)
        eugene.countries_dict['Ireland'] = 1

        country, maximum = mike.get_country_and_maximum_assignments()
        self.assertEqual(country, 'Croatia')
        self.assertEqual(maximum, 1)

        country, maximum = eugene.get_country_and_maximum_assignments()
        self.assertEqual(country, 'Ireland')
        self.assertEqual(maximum, 1)

        ret_val = is_there_duplicate_countries([mike, eugene])
        self.assertFalse(ret_val)

    def test_is_there_duplicate_countries_runtime_error(self):
        with self.assertRaises(RuntimeError):
            is_there_duplicate_countries([], count=2, limit=1)
