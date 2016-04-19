# -*- coding: utf-8 -*-
from unittest2 import TestCase

from ..utils import sanitize_string


class TestUtils(TestCase):

    def test_sanitize_string(self):
        test_cases = (
            ('Côte d’Ivoire', 'C_te_d_Ivoire'),
            ('United Kingdom', 'United_Kingdom'),
            ('<foo val=“bar” />', '_foo_val__bar____')
        )

        for name, expected in test_cases:
            self.assertEqual(
                sanitize_string(name),
                expected,
                'Testing string: {}'.format(name)
            )
