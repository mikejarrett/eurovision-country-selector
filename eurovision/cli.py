# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
import sys
import argparse

from .eurovision import (
    add_countries_to_people,
    get_countries_from_csv,
    is_there_duplicate_countries,
    print_results,
    write_data_to_csv
)

from .person import (
    build_list_of_people,
    build_list_of_people_from_csv
)

from .utils import sanitize_string


COUNTRIES_CSV_FILEPATH = 'eurovision/data/countries-2016.csv'


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Select countries for people when watching EuroVision.',
        add_help=True
    )
    parser.add_argument(
        '--countries',
        default=None,
        nargs='?',
        type=str,
        help='The csv file of countries to that are in the competition.'
    )
    parser.add_argument(
        '--countrieslist',
        nargs='?',
        type=str,
        help='Names of countries that are in the competition.'
    )
    parser.add_argument(
        '--people',
        default=None,
        nargs='?',
        type=str,
        help=(
            'The csv file which contains people names and their countries '
            'to exclude.'
        )
    )
    parser.add_argument(
        '--peoplelist',
        nargs='+',
        type=str,
        help='Names of people that will be attending the party.'
    )
    parser.add_argument(
        '--outfile',
        default='eurovision.csv',
        nargs='?',
        help='The filename to save results to.'
    )
    parser.add_argument(
        '--loops',
        default=1000,
        nargs=1,
        type=int,
        help='Number of times to loop the check.'
    )
    args = parser.parse_args()

    if args.countrieslist:
        countries = [
            sanitize_string(country)
            for country in args.countries
        ]
    elif args.countries:
        try:
            countries = get_countries_from_csv(args.countries)
        except OSError as err:
            print(err)
            sys.exit(255)
    else:
        try:
            countries = get_countries_from_csv(COUNTRIES_CSV_FILEPATH)
        except OSError:
            message = "Couldn't find included countries: {}"
            print(message.format(COUNTRIES_CSV_FILEPATH))
            sys.exit(255)

    if args.people:
        people = build_list_of_people_from_csv(
            filename=args.people,
            countries=countries
        )
    elif args.peoplelist:
        names = args.peoplelist
        people = build_list_of_people(
            names,
            countries,
            excluded_countries=None
        )
    else:
        parser.print_help()
        sys.exit(1)

    people = add_countries_to_people(people, countries, args.loops)

    count = 1
    while not is_there_duplicate_countries(people, count, limit=10):
        people = add_countries_to_people(people, countries, args.loops)
        count += 1

    if args.outfile:
        write_data_to_csv(args.outfile, people, countries)

    print_results(people)

if __name__ == '__main__':
    main()
