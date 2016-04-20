# -*- coding: utf-8 -*-
from os import path
from random import choice, shuffle
import copy
import csv

from .utils import sanitize_string


def get_countries_from_csv(filepath):
    """ Process a csv countaining country data.

    Args:
        filepath (str): A path to a csv file.

    Returns:
        list: sanitized country names as strings.

    Raises:
        OSError: If file does not exist at the filepath.
    """
    if not path.exists(filepath):
        raise OSError('Path to file: "{}" does not exist.'.format(filepath))

    with open(filepath, 'r') as csv_file:
        reader = csv.reader(csv_file)
        return [sanitize_string(''.join(row)) for row in reader]


def add_countries_to_people(people, countries, loop_count=1000):
    """ Add country data to people.

    Shuffle ``people`` list order and loop through the the list of people
    ``loop_count`` times.

    Randomly select a country from the ``countries`` list. If the country
    is in the person's ``excluded_countries`` list, randomly select a new
    country until a valid country is selected.

    Once a valid country is selected, increment the count for that country
    on the person.

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
            inifity_buster = 0
            while country in person.excluded_countries:
                country = choice(_countries)
                inifity_buster += 1

                # Prevent infinite loops!
                if inifity_buster > 100:
                    raise RuntimeError(
                       "Couldn't find a country that is not in "
                       "{}'s excluded_countries".format(person.name)
                    )

            _countries.remove(country)
            person.increment_country_hit(country)

    return people


def write_data_to_csv(csv_name, people, countries):
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


def print_results(people):  # pragma: no cover
    """ Loop through the list of people and print them to console.

    Args:
        people (list): List of instantiated ``Person`` objects.
    """
    for person in people:
        country, maximum = person.get_country_and_maximum_assignments()
        print('{} -- {} ({})'.format(person.name, country, maximum))
