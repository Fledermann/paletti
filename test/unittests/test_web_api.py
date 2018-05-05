#!/usr/bin/env python

""" Unittests for the web_api module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner
(paletti/paletti/test/unittest_run.py) instead. """

import unittest

from paletti import web_api


class TestSiteAPI(unittest.TestCase):

    def test__make_filename(self):
        # The result should be a dict.
        fn = web_api._make_filename('8Ä;ä0ß33nfkjdksnad')
        self.assertIsInstance(fn, str)
