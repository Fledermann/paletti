#!/usr/bin/env python

import unittest

import _example_plugin


class TestExample(unittest.TestCase):

    def test_parse_userinput(self):
        userpage = 'https://example.com/user/NickCage'
        query = 'What am I doing with my life part IV'
        self.assertEqual(_example_plugin.parse_userinput(userpage), 'user')
        self.assertEqual(_example_plugin.parse_userinput(query), 'search_query')
