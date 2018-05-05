#!/usr/bin/env python

""" Unittests for the `utils` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import tempfile
import unittest
from unittest.mock import patch, Mock

import paletti.utils


class TestDownload(unittest.TestCase):

    @patch('utils.urllib3.PoolManager.request', autospec=True)
    def setUp(self, mock_request):
        tmp = tempfile.NamedTemporaryFile()
        mock_request.return_value.headers = {'Content-Length': 1}
        self.dl = paletti.utils.Downloader('http://example.com', tmp.name)

    @patch('utils.urllib3.PoolManager.request', autospec=True)
    def test_start_download(self,  mock_request):
        # Mock a response stream to not download a real file
        mock_request.return_value.stream.return_value = [b'12345', b'']
        result = self.dl.start()
        self.assertEqual(result, None)

    @patch('utils.urllib3.PoolManager.request', autospec=True)
    def test_cancel_download(self, mock_request):
        mock_request.return_value.stream.return_value = [b'12345', b'']
        result = self.dl.start()
        self.assertEqual(self.dl.cancel(), None)



