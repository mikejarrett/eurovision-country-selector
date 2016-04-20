# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from unittest2 import TestCase

from ..person import (
    Person,
    build_list_of_people,
    build_list_of_people_from_csv,
)


class TestPersonObject(TestCase):

    def test_person(self):
        person = Person('Mike', ['Ireland', 'Croatia'])
        person.increment_country_hit('Ireland')
        ret_val = person.get_country_and_maximum_assignments()
        expected = ('Ireland', 1)
        self.assertEqual(ret_val, expected)
        self.assertEqual(person.Croatia, 0)

    def test_person_no_countries(self):
        person = Person('Mike', None)
        self.assertEqual(person.countries, [])


class TestHelperFunctions(TestCase):

    def setUp(self):
        self.countries = ['Ireland', '__dict__']

    def test_build_list_of_people_from_csv_no_exclude(self):
        ret_val = build_list_of_people_from_csv(
            'eurovision/tests/csv/names_no_exclude.csv',
            self.countries
        )
        self.assertEqual(len(ret_val), 4)
        for person in ret_val:
            self.assertEqual(person.excluded_countries, [])

    def test_build_list_of_people_from_csv_with_exclude(self):
        ret_val = build_list_of_people_from_csv(
            'eurovision/tests/csv/names_with_exclude.csv',
            self.countries
        )
        self.assertEqual(len(ret_val), 4)
        for person in ret_val:
            self.assertTrue(person.excluded_countries != [])

    def test_build_list_of_people(self):
        ret_val = build_list_of_people(['Mike', 'Bill'], self.countries)
        self.assertEqual(len(ret_val), 2)
        for person in ret_val:
            self.assertTrue(hasattr(person, 'Ireland'))

    def test_build_list_of_people_with_excluded_countries(self):
        ret_val = build_list_of_people(
            ['Mike', 'Bill'],
            self.countries,
            ['Croatia']
        )
        self.assertEqual(len(ret_val), 2)
        for person in ret_val:
            self.assertTrue(hasattr(person, 'Ireland'))
            self.assertEqual(person.excluded_countries, ['Croatia'])
