#!/usr/bin/env python

""" Runner for all unittests.

"""

import pathlib
import unittest
import sys

root = pathlib.Path(__file__).resolve().parent.parent
tests = pathlib.Path(__file__).parent / 'unittests'
sys.path.append(str(root))
sys.path.append(str(tests))

import test_downloader
import test_main
import test_utils
import test_web_api

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_downloader))
suite.addTests(loader.loadTestsFromModule(test_main))
suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_web_api))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)