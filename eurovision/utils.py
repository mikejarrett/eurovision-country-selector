# -*- coding: utf-8 -*-
import re


def sanitize_string(string):
    """ Take a string and remove replace all chars that aren't a letter. """
    return re.sub(r'[^a-zA-Z]', '_', string)
