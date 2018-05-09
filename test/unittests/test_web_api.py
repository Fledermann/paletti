#!/usr/bin/env python

""" Unittests for the `web_api` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest
from unittest import mock

from paletti import web_api


class TestWebAPI(unittest.TestCase):

    def test_download(self):
        web_api.streams = mock.Mock(return_value={'title': 'mock'})
        web_api.metadata = mock.Mock(return_value={'title': 'mock'})
        web_api.Download = mock.Mock()
        self.assertIsInstance(web_api.download('https://example.com', '/tmp'), mock.Mock)

    def test_user(self):
        # The result should be a dict.
        self.assertRaises(ModuleNotFoundError, lambda: web_api.user('foo', 'bar'))
