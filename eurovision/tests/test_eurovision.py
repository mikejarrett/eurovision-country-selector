# -*- coding: utf-8 -*-
import os

from unittest2 import TestCase

from ..eurovision import (
    add_countries_to_people,
    get_countries_from_csv,
    write_data_to_csv_print_results
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
        expected = ['Ireland', 'Sweden']
        self.assertEqual(countries, expected)

    def test_add_countries_to_people(self):
        ret_val = add_countries_to_people(
            self.people,
            self.countries,
            loop_count=1
        )
        person = ret_val[0]
        self.assertEqual(person.name, 'Mike')
        self.assertEqual(person.Ireland, 1)

    def test_add_countries_to_people_no_endless_loop(self):
        people = [Person('Mike', self.countries, self.countries)]
        with self.assertRaises(RuntimeError):
            add_countries_to_people(people, self.countries, loop_count=1)

    def test_write_data_to_csv_print_results(self):
        write_data_to_csv_print_results(
            'test.csv',
            self.people,
            self.countries
        )
        with open('test.csv', 'r') as test_csv:
            self.assertEqual(
                test_csv.read().replace('\n', ''),
                'name,IrelandMike,0'
            )
        os.remove('test.csv')
