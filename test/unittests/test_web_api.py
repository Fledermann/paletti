#!/usr/bin/env python

""" Unittests for the `web_api` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import importlib
import unittest
from collections import namedtuple
from unittest import mock

from paletti import web_api


class TestWebAPI(unittest.TestCase):

    def setUp(self):
        # We need some set up to mock the decorators appropiately.
        # Throughout these tests, our mocked plugin will be called
        # 'cool_plugin' and its website is 'http://example.com'
        mod_file = namedtuple('mod_file', ['name'])
        module = namedtuple('module', ['HOSTS', 'STREAM_TYPE', 'playlist',
                                       'search', 'get_metadata', 'parse_userinput'])
        cool_plugin = mod_file(name='cool_plugin')
        parse_ui = mock.Mock()
        parse_ui.return_value = 'search_query'
        mod = module(HOSTS=['example.com'], STREAM_TYPE='audio+video',
                     playlist=mock.Mock(), search=mock.Mock(),
                     get_metadata=mock.Mock(), parse_userinput=parse_ui)
        mock_pkgs = [cool_plugin]
        web_api.pkgutil.walk_packages = mock.Mock(return_value=mock_pkgs)
        web_api.importlib.import_module = mock.Mock(return_value=mod)

        def kill_patches():
            mock.patch.stopall()
            importlib.reload(web_api)

        self.addCleanup(kill_patches)
        mock.patch('paletti.web_api.module', lambda x: x).start()
        importlib.reload(web_api)

    def test__filter_stream(self):
        streams = [{'id': 1, 'type': 'video', 'container': 'webm',
                    'quality': '1080p', 'quality_int': '1080'},
                   {'id': 2, 'type': 'video', 'container': 'webm',
                    'quality': '720p', 'quality_int': '720'},
                   {'id': 3, 'type': 'audio+video', 'container': 'mp4',
                    'quality': '720p', 'quality_int': '720'}
                   ]
        filtered = web_api._filter_stream(streams, 'video', '720p', 'webm')
        self.assertEqual(filtered['id'], 2)
        filtered = web_api._filter_stream(streams, 'audio', 'best', 'webm')
        self.assertTrue(filtered is None)
        filtered = web_api._filter_stream(streams, 'video', '480p', 'mp4')
        self.assertEqual(filtered['id'], 3)

    def test__playlist(self):
        playlist = web_api._playlist('http://example.com/123')
        self.assertIsNotNone(playlist)

    def test_cache(self):
        @web_api.cache
        def f(plugin, testitem):
            return {'url': testitem}
        self.assertIsInstance(f('foo', 'http://example.com/213'), dict)
        self.assertIsInstance(f('foo', 'http://example.com/123'), dict)

    def test_channel(self):
        url = 'http://example.com/123'
        self.assertRaises(NotImplementedError, lambda: web_api.channel(url))

    def test_download(self):
        web_api.streams = mock.Mock(return_value={'title': 'mock'})
        web_api.metadata = mock.Mock(return_value={'title': 'mock'})
        web_api.Download = mock.Mock()
        self.assertIsInstance(web_api.download('https://example.com', '/tmp'), mock.Mock)

    def test_metadata(self):
        md = web_api.metadata('http://example.com/123')
        self.assertIsNotNone(md)

    def test_module(self):
        @web_api.module
        def f(plugin, testitem):
            return {'url': 'testitem'}
        self.assertIsInstance(f('cool_plugin', 'search query'), dict)
        self.assertIsInstance(f('http://example.com/123'), dict)
        self.assertRaises(ModuleNotFoundError, lambda: f('no_plugin', '-'))

    def test_search(self):
        result = web_api.search('cool_plugin', 'How to shave a ferret')


    @mock.patch('builtins.open', create=False)
    def test_thumbnail(self, mock_open):
        md = {'id': '12345', 'thumbnail_small': 'http://example.com/thumb.jpg'}
        web_api.metadata = mock.Mock(return_value=md)
        web_api.urllib3.PoolManager = mock.Mock()
        web_api.urllib3.PoolManager.return_value.request.return_value.data = b'12345'

        with mock.patch('web_api.open', mock.mock_open()):
            self.assertEqual(web_api.thumbnail('http://example.com/123'), '/tmp/12345.jpg')

    def test_user(self):
        url = 'http://example.com/123'
        self.assertRaises(NotImplementedError, lambda: web_api.user(url))
