#!/usr/bin/env python

""" Unittests for the `main` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest
from unittest import mock

from paletti import main


class TestMain(unittest.TestCase):

    @mock.patch('builtins.open', create=False)
    def test_get_plugins_from_repo(self, mock_open):
        data = b'plugin_one\nplugin_two\n_example_plugin'

        main.urllib3.HTTPSConnectionPool = mock.Mock()
        main.urllib3.HTTPSConnectionPool.return_value.request.return_value.data = data

        url = 'https:/github.com/example/example'
        self.assertIsInstance(main.get_plugins_from_repo(url), list)