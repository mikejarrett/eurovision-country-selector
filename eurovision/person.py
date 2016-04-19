# -*- coding: utf-8 -*-
import csv
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


def build_list_of_people_from_csv(filename, countries):
    people = []
    with open(filename, 'r') as opened_file:
        reader = csv.reader(opened_file)
        for row in reader:
            excluded_countries = []
            if len(row) > 1:
                excluded_countries = [
                    sanitize_string(name)
                    for name in row[1].split(',')
                ]
            people.append(
                Person(
                    name=row[0],
                    countries=countries,
                    excluded_countries=excluded_countries
                )
            )

    return people


def build_list_of_people(people, countries, excluded_countries=None):
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
    if excluded_countries is None:
        excluded_countries = []

    return [
        Person(name, countries, excluded_countries)
        for name in people
    ]


def sanitize_string(string):
    return re.sub(r'[^a-zA-Z]', '_', string)
