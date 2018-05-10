#!/usr/bin/env python

""" Unittests for the `main` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import time
import unittest
from unittest import mock

from paletti import downloader


class TestDownloader(unittest.TestCase):

    def setUp(self):

        # Mock the download stream. We're pretending to download a file
        # of 132000 bytes, which means one full and on partial chunk
        # for urllib3.request.stream(1024*128).
        def mock_stream():
            yield b' ' * (1024*128-33)
            time.sleep(0.02)
            yield b' ' * 895

        streams = ({},
                   {'url': 'http://example.com/audio.mp3',
                    'title': 'Foo',
                    'codec': 'vp9',
                    'type': 'video',
                    'container': 'wbm'})
        outfile = '/tmp/foobar'
        data = b''
        headers = {'Content-Length': '132000'}
        stream = mock_stream()
        downloader.urllib3.PoolManager = mock.Mock()
        downloader.urllib3.PoolManager.return_value.request.return_value.data = data
        downloader.urllib3.PoolManager.return_value.request.return_value.stream.return_value = stream
        downloader.urllib3.PoolManager.return_value.request.return_value.headers = headers

        self.dl = downloader.Download(streams, outfile, mock.Mock)
        self.dl2 = downloader.Download(streams, outfile, mock.Mock)
        self.assertEqual(self.dl.status, 'idle')

    @mock.patch('builtins.open', create=False)
    def test_start(self, mock_open):
        # Start a download, check it's properties, and wait for it to finish.
        self.dl.start()
        self.assertEqual(self.dl.status, 'active')
        self.assertEqual(self.dl.filesize, 132000)
        self.assertIsInstance(repr(self.dl), str)
        while self.dl.status == 'active':
            pass
        self.assertEqual(self.dl.progress, self.dl.filesize)

    def test_cancel(self):
        # Start a new download and cancel it immediately.
        self.dl2.start()
        self.dl2.cancel()
        self.assertEqual(self.dl2.status, 'cancelled')