#!/usr/bin/env python

""" Unittests for the `utils` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest

from paletti import utils


class TestUtils(unittest.TestCase):

    def test_make_filename(self):
        self.assertIsInstance(utils.make_filename('aw iw))(""23+*.,!!'), str)
