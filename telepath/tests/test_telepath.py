#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_telepath
----------------------------------

Tests for `telepath` module.
"""

import argparse
import unittest

from telepath import telepath

import mock
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

    def test_missing_status_file_returns_empty_status(self):
        mo = mock.mock_open()
        mo.side_effect = IOError("File does not exist!")
        with mock.patch('{}.open'.format(__name__), mo, create=True):
            return_value = telepath.get_completed_tasks("status_filename.txt")
            self.assertEqual('', return_value)

    @mock.patch.object(telepath, 'post_data_to_endpoint')
    @mock.patch.object(telepath, 'get_completed_tasks')
    def test_send_report_wont_send_empty_report(self,
                                                get_completed_mock,
                                                post_mock):
        get_completed_mock.return_value = ''
        telepath.send_report(argparse.Namespace(), self.good_config)
        self.assertTrue(post_mock.call_count == 0)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
