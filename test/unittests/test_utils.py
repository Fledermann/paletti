#!/usr/bin/env python

""" Unittests for the `utils` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest
from unittest import mock

from paletti import utils


class TestUtils(unittest.TestCase):

    def test_make_filename(self):
        self.assertEqual(utils.make_filename('aw iw))(""23+*.,!!'), 'aw_iw_23_')

    def test_merge_files(self):
        mock_listdir = ['foo.webm.video.vp9', 'bar.mp4.audio.aac',
                        'bar.mp4.video.ac1', 'baz.webm.audio.opus',
                        'otherfile.txt', 'something.log.2.old']
        utils.os.listdir = mock.Mock(return_value=mock_listdir)
        utils.os.rename = mock.Mock()
        utils.os.remove = mock.Mock()
        utils.subprocess.call = mock.Mock()
        self.assertEqual(utils.merge_files('foo'), 'foo.vp9')
        self.assertEqual(utils.merge_files('bar'), 'bar.mp4')
        self.assertEqual(utils.merge_files('baz'), 'baz.opus')

