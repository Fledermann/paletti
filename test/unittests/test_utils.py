#!/usr/bin/env python

""" Unittests for the `utils` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest
from unittest import mock

from paletti import utils


class TestUtils(unittest.TestCase):

    def test_make_filename(self):
        self.assertIsInstance(utils.make_filename('aw iw))(""23+*.,!!'), str)

    def test_merge_files(self):
        utils.os.listdir = mock.Mock(return_value=['foo.webm.video.vp9'])
        utils.os.rename = mock.Mock()
        self.assertIsInstance(utils.merge_files('/tmp/foo'), str)
