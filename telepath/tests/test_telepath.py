#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_telepath
----------------------------------

Tests for `telepath` module.
"""

import unittest

from telepath import telepath

from six.moves import configparser

GOOD_CONFIGURATION_OPTIONS = {
    'endpoint': 'http://goodstandupendpoint.com',
    'irc_nick': 'clif_h',
    'status_filename': 'mystatusstore.txt'
}


class TestTelepath(unittest.TestCase):

    def setUp(self):
        pass

    def test_telepath_validate_configuration_good(self):
        config = configparser.ConfigParser()
        config.add_section('telepath')
        for key, value in GOOD_CONFIGURATION_OPTIONS.items():
            config.set('telepath', key, value)
        is_config_good, reason = telepath.validate_configuration(config)
        self.assertTrue(is_config_good)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
