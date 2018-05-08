#!/usr/bin/env python

""" Unittests for the `web_api` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest

from paletti import web_api


class TestWebAPI(unittest.TestCase):

    def test_user(self):
        # The result should be a dict.
        self.assertRaises(NotImplementedError, lambda: web_api.user('youtube', 'bar'))
