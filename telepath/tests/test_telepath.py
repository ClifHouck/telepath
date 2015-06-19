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
        self.good_config = self._get_good_config()

    def _get_good_config(self):
        config = configparser.ConfigParser()
        config.add_section('telepath')
        for key, value in GOOD_CONFIGURATION_OPTIONS.items():
            config.set('telepath', key, value)
        return config

    def test_telepath_validate_configuration_good(self):
        config = self.good_config
        is_config_good, reason = telepath.validate_configuration(config)
        self.assertTrue(is_config_good, reason)

    def test_configuration_has_no_telepath_section(self):
        config = self.good_config
        config.remove_section('telepath')
        is_config_good, reason = telepath.validate_configuration(config)
        self.assertFalse(is_config_good, reason)

    def test_configuration_missing_required_option(self):
        config = self.good_config
        config.remove_option('telepath', 'irc_nick')
        is_config_good, reason = telepath.validate_configuration(config)
        self.assertFalse(is_config_good, reason)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
