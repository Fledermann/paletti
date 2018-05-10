#!/usr/bin/env python

""" Unittests for the `web_api` module. To avoid path problems and for
convienience, this module shouldn't be run directly, use the runner instead.
"""

import unittest
from collections import namedtuple
from unittest import mock

from paletti import web_api


class TestWebAPI(unittest.TestCase):

    def test_cache(self):
        @web_api.cache
        def f(plugin, testitem):
            return {'url': testitem}
        self.assertIsInstance(f('foo', 'http://bar'), dict)
        self.assertIsInstance(f('foo', 'http://bar'), dict)

    def test_module(self):
        mod_file = namedtuple('mod_file', ['name'])
        module = namedtuple('module', ['HOSTS', 'STREAM_TYPE'])
        cool_plugin = mod_file(name='cool_plugin')
        mod = module(HOSTS=['b.foo.com'], STREAM_TYPE='audio+video')
        mock_pkgs = [cool_plugin]

        web_api.pkgutil.walk_packages = mock.Mock(return_value=mock_pkgs)
        web_api.importlib.import_module = mock.Mock(return_value=mod)

        @web_api.module
        def f(plugin, testitem):
            return {'url': 'testitem'}
        self.assertIsInstance(f('cool_plugin', 'http://bar'), dict)
        self.assertIsInstance(f('cool_plugin', 'http://bar'), dict)
        self.assertRaises(ModuleNotFoundError, lambda: f('no_plugin', 'http://bar'))


    def test_download(self):
        web_api.streams = mock.Mock(return_value={'title': 'mock'})
        web_api.metadata = mock.Mock(return_value={'title': 'mock'})
        web_api.Download = mock.Mock()
        self.assertIsInstance(web_api.download('https://example.com', '/tmp'), mock.Mock)

    def test_user(self):
        # The result should be a dict.
        self.assertRaises(ModuleNotFoundError, lambda: web_api.user('foo', 'bar'))
