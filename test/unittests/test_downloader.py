#!/usr/bin/env python

""" Unittests for the `main` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import time
import unittest
from unittest import mock

from paletti import downloader


class TestDownload(unittest.TestCase):

    def setUp(self):

        def mock_stream():
            for i in range(10):
                time.sleep(0.01)
                yield i

        streams = ({},
                   {'url': 'http://example.com/audio.mp3',
                    'title': 'Foo',
                    'codec': 'vp9',
                    'type': 'video',
                    'container': 'wbm'})
        outfile = '/tmp/foobar'
        data = b''
        headers = {'Content-Length': '2048'}
        stream = mock_stream()
        downloader.urllib3.PoolManager = mock.Mock()
        downloader.urllib3.PoolManager.return_value.request.return_value.data = data
        downloader.urllib3.PoolManager.return_value.request.return_value.stream.return_value = stream
        downloader.urllib3.PoolManager.return_value.request.return_value.headers = headers

        self.dl = downloader.Download(streams, outfile, mock.Mock)
        self.assertEqual(self.dl.status, 'idle')

    @mock.patch('builtins.open', create=False)
    def test_start(self, mock_open):
        self.dl.start()
        self.assertEqual(self.dl.status, 'active')
        self.assertEqual(self.dl.filesize, 2048)

    def test_cancel(self):
        self.dl.cancel()
        self.assertEqual(self.dl.status, 'cancelled')