# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
import argparse

from eurovision import EuroVision

from person import (
    build_list_of_people,
    build_list_of_people_from_csv,
    sanitize_country_name
)


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
            sanitize_country_name(country)
            for country in args.countries
        ]
    else:
        countries = EuroVision.COUNTRIES

    if args.infile:
        people = build_list_of_people_from_csv(
            filename=args.infile,
            countries=countries
        )
    elif args.names:
        names = args.names
        people = build_list_of_people(
            names,
            countries,
            excluded_countries=None
        )

    people = EuroVision.add_countries_to_people(people, countries, args.loops)
    EuroVision.write_data_to_csv_print_results(args.outfile, people, countries)
