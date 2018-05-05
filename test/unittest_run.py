#!/usr/bin/env python

""" Runner for all unittests.

"""
import os
import unittest
import sys

root_path = os.path.abspath('../')
sys.path.append(root_path)

from unittests import test_utils
from unittests import test_web_api

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_web_api))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)