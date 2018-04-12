#!/usr/bin/env python

""" Unittests for the web_api module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner
(paletti/paletti/test/runner.py) instead. """

import unittest

import paletti.web_api


class TestSiteAPI(unittest.TestCase):

    def setUp(self):
        self.site_api = paletti.web_api.SiteAPI('foobar')

    def test_get_information(self):
        # The result should be a dict.
        information = self.site_api.get_information('http://example.com')
        self.assertIsInstance(information, dict)

    def test_search(self):
        # The result should be a list.
        self.assertIsInstance(self.site_api.search('query'), list)

    def test_wrong_plugin(self):
        # Creating an SiteAPI instance with a non-existant plugin should
        # raise a ModuleNotFoundError.
        with self.assertRaises(ModuleNotFoundError):
            paletti.web_api.SiteAPI('12345')
