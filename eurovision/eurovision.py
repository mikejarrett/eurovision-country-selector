#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, shuffle
import copy
import csv


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
        with open(csv_name, 'w') as outfile:
            writer = csv.writer(outfile)
            columns = ['name'] + countries
            writer.writerow(columns)
            for person in people:
                person_row = [person.name] + [
                    getattr(person, country, 0) for country in countries
                ]
                writer.writerow(person_row)

                country, maximum = person.get_country_and_maximum_assignments()

                print(
                    '{} -- {} ({})'.format(
                        person.name,
                        country,
                        maximum
                    )
                )
