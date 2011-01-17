#!/usr/bin/env python
# -*- coding: utf8 -*-
"""

Test for Nonius Kappa CCD cameras.

"""

import unittest
import os
import logging
import sys
import numpy

for idx, opts in enumerate(sys.argv[:]):
    if opts in ["-d", "--debug"]:
        logging.basicConfig(level=logging.DEBUG)
        sys.argv.pop(idx)
try:
    logging.debug("tests loaded from file: %s" % __file__)
except:
    __file__ = os.getcwd()

from utilstest import UtilsTest
from fabio.kcdimage     import kcdimage
from fabio.edfimage     import edfimage
from fabio.openimage    import openimage



class testkcd(unittest.TestCase):
    """basic test"""
    kcdfilename = 'i01f0001.kcd'
    edffilename = 'i01f0001.edf'
    results = """i01f0001.kcd   625 576  96  66814.0 195.3862972   243.58150990245315"""


    def setUp(self):
        """Download files"""
        UtilsTest.getimage(self.kcdfilename)
        UtilsTest.getimage(self.edffilename)

    def test_read(self):
        """ check we can read kcd images"""
        vals = self.results.split()
        name = vals[0]
        dim1, dim2 = [int(x) for x in vals[1:3]]
        mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
        obj = openimage(os.path.join("testimages", name))
        self.assertAlmostEqual(mini, obj.getmin(), 2, "getmin")
        self.assertAlmostEqual(maxi, obj.getmax(), 2, "getmax")
        self.assertAlmostEqual(mean, obj.getmean(), 2, "getmean")
        self.assertAlmostEqual(stddev, obj.getstddev(), 2, "getstddev")
        self.assertEqual(dim1, obj.dim1, "dim1")
        self.assertEqual(dim2, obj.dim2, "dim2")


    def test_same(self):
        """ see if we can read kcd images and if they are the same as the EDF """
        kcd = kcdimage()
        kcd.read(os.path.join("testimages", self.kcdfilename))
        edf = edfimage()
        edf.read(os.path.join("testimages", self.edffilename))
        diff = (kcd.data.astype("int32") - edf.data.astype("int32")).ravel()
        self.assertAlmostEqual(numpy.max(diff), 0, 2)


def test_suite_all_kcd():
    testSuite = unittest.TestSuite()
    testSuite.addTest(testkcd("test_read"))
    testSuite.addTest(testkcd("test_same"))
    return testSuite

if __name__ == '__main__':
    mysuite = test_suite_all_kcd()
    runner = unittest.TextTestRunner()
    runner.run(mysuite)