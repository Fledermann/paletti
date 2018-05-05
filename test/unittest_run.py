#!/usr/bin/env python

""" Runner for all unittests.

"""

import pathlib
import unittest
import sys

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(root))

from unittests import test_utils
from unittests import test_web_api

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_web_api))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)