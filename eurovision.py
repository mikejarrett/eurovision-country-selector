#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, shuffle
import argparse
import copy
import csv
import operator
import re


class Person(object):

    def __init__(self, name, countries, excluded_countries=None):
        """ Initiate a ``Person`` object.

        Args:
            name (str): Name of the person.
            countries (list): Countries to be used as attributes on the class.
            excluded_countries (Optional(list)): List of countries to be
                excluded when running the check.
        """
        self.name = name

        if excluded_countries is None:
            excluded_countries = []
        self.excluded_countries = excluded_countries

        if countries is None:
            countries = []
        self.countries = countries
        for country in countries:
            setattr(self, country, 0)

    def get_country_and_maximum_assignments(self):
        """ Retrieve the country with the maximum number of hits.

        Returns:
            tuple: (country_name, maximum) where maximum is the number of hits.
        """
        maximum = 0
        country_name = ''
        for country in self.countries:
            value = getattr(self, country, 0)
            if value > maximum:
                maximum = value
                country_name = country

        return country_name, maximum

    def increment_country_hit(self, country):
        count = getattr(self, country, 0) + 1
        setattr(self, country, count)


class EuroVision:

    COUNTRIES = [
        'Albania',
        'Armenia',
        'Australia',
        'Austria',
        'Azerbaijan',
        'Belarus',
        'Belgium',
        'Bosnia_and_Herzegovina',
        'Bulgaria',
        'Croatia',
        'Cyprus',
        'Czech Republic',
        'Denmark',
        'Estonia',
        'F_Y_R_Macedonia',
        'Finland',
        'France',
        'Georgia',
        'Germany',
        'Greece',
        'Hungary',
        'Iceland',
        'Ireland',
        'Israel',
        'Italy',
        'Latvia',
        'Lithuania',
        'Malta',
        'Moldova',
        'Montenegro',
        'Norway',
        'Poland',
        'Romania',
        'Russia',
        'San_Marino',
        'Serbia',
        'Slovenia',
        'Spain',
        'Sweden',
        'Switzerland',
        'The_Netherlands',
        'Ukraine',
        'United_Kingdom'
    ]

    @classmethod
    def _get_names_and_exclude_countries_from_csv_filename(cls, filename, countries):
        people = []
        with open(filename, 'r') as opened_file:
            reader = csv.reader(opened_file)
            for row in reader:
                excluded_countries = [
                    cls._sanitize_country_name(name)
                    for name in row[1].split(',')
                ]
                people.append(
                    Person(
                        name=row[0],
                        countries=countries,
                        excluded_countries=excluded_countries
                    )
                )

            import ipdb; ipdb.set_trace()
        return people

    @classmethod
    def _sanitize_country_name(cls, name):
        return re.sub(r'[^a-zA-Z]', '_', name)

    @classmethod
    def build_list_of_people(
        cls,
        people,
        countries=COUNTRIES,
        excluded_countries=None,
    ):
        """
        Args:
            people (list): List of strings representing names.
            countries (Optional(list)): List of countries that will be used to
                build dynamic attributes.
            excluded_countries (Optional(list)): List of countries to that
                the person should not select.

        Returns:
            list: List of ``Person`` objects.
        """
        if countries is None:
            countries = []

        if excluded_countries is None:
            excluded_countries = []

        return [
            Person(name, countries, excluded_countries)
            for name in people
        ]


    @classmethod
    def add_countries_to_people(cls, people, countries, loop_count=1000):
        """ Add country data to people.

        Shuffle ``people`` list order and loop through the the list of people
        ``loop_count`` times.

        Randomly select a country from the ``countries`` list. If the country
        is in the person's ``excluded_countries`` list, randomly select a new
        country until a valid country is selected.

        Once a valid country is selected, increment the count for that country
        on the person.

        Call ``write_data_to_csv_print_results`` to write the data to a csv and
        print the results.

        Args:
            people (list): List of instantiated ``Person`` objects.
            countries (list): List of strings that represent countries.
            loop_count (Optional[int]): The number of times to run the test.

        Returns:
            list: List of ``Person`` objects with updated countries counts.
        """
        shuffle(people)
        for __ in range(loop_count):
            _countries = copy.deepcopy(countries)
            for person in people:
                count = 0
                country = choice(_countries)
                while country in person.excluded_countries:
                    country = choice(_countries)

                _countries.remove(country)
                person.increment_country_hit(country)

        return people


    @classmethod
    def write_data_to_csv_print_results(cls, csv_name, people, countries):
        """ Loop through the list of people and write them to a csv.

        Args:
            csv_name (str): Name of the file to write results to.
            people (list): List of instantiated ``Person`` objects.
            countries (list): List of strings that represent countries.
        """
        with open(csv_name, 'w') as ev:
            writer = csv.writer(ev)
            columns = ['name'] + countries
            writer.writerow(columns)
            for person in people:
                person_row = [person.name] + [
                    getattr(person, country, 0) for country in countries
                ]
                writer.writerow(person_row)

                country, maximum = person.get_country_and_maximum_assignments()
                print('{} -- {} ({})'.format(person.name, country, maximum))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Select countries for people when watching EuroVision.',
        add_help=True
    )
    parser.add_argument(
        '--names',
        nargs='+',
        type=str,
        help='Names that we want to select countries for.'
    )
    parser.add_argument(
        '--loops',
        default=1000,
        nargs=1,
        type=int,
        help='Number of times to loop the check.'
    )
    parser.add_argument(
        '--countries',
        nargs='+',
        type=str,
        help='List of countries we want to use.'
    )
    parser.add_argument(
        '--infile',
        default=None,
        nargs='?',
        type=str,
        help='The file which contains people names and countries to exclude.'
    )
    parser.add_argument(
        '--outfile',
        default='eurovision.csv',
        nargs='?',
        help='The filename to save results to.'
    )
    args = parser.parse_args()

    if args.countries:
        countries = [
            EuroVision._sanitize_country_name(country)
            for country in args.countries
        ]
    else:
        countries = EuroVision.COUNTRIES

    if args.infile:
        people = EuroVision._get_names_and_exclude_countries_from_csv_filename(
            filename=args.infile,
            countries=countries
        )
    elif args.names:
        names = args.names
        people = EuroVision.build_list_of_people(
            names,
            countries,
            excluded_countries=None
        )

    people = EuroVision.add_countries_to_people(people, countries, args.loops)
    EuroVision.write_data_to_csv_print_results(args.outfile, people, countries)
