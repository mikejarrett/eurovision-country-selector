EuroVision Country Selector
===========================

Select a country for your EuroVision party.

Useage
------

    $ eurovision --people people.csv  --outfile whos-got-what.csv
    Mike -- Hungary (36)


    usage: eurovision-script.py [-h] [--countries [COUNTRIES]]
                                [--countrieslist [COUNTRIESLIST]]
                                [--people [PEOPLE]]
                                [--peoplelist PEOPLELIST [PEOPLELIST ...]]
                                [--outfile [OUTFILE]] [--loops LOOPS]

    Select countries for people when watching EuroVision.

    optional arguments:
      -h, --help            show this help message and exit
      --countries [COUNTRIES]
                            The csv file of countries to that are in the
                            competition.
      --countrieslist [COUNTRIESLIST]
                            Names of countries that are in the competition.
      --people [PEOPLE]     The csv file which contains people names and their
                            countries to exclude.
      --peoplelist PEOPLELIST [PEOPLELIST ...]
                            Names of people that will be attending the party.
      --outfile [OUTFILE]   The filename to save results to.
      --loops LOOPS         Number of times to loop the check.


Example Data
------------

* https://github.com/mikejarrett/eurovision-country-selector/tree/master/examples/