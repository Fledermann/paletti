#!/usr/bin/env python

import os
import unittest
import sys

root_path = os.path.abspath('../')
sys.path.append(root_path)

import functional
import test_utils
import test_web_api

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_web_api))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)