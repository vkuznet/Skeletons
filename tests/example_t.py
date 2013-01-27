#!/usr/bin/env python
#pylint: disable-msg=c0301,c0103

'''
unit test example
'''

import sys
import unittest

def fail_function(value):
    return 1./value

class testExample(unittest.TestCase):
    "A test class"
    def setUp(self):
        "set up"
        # some stuff to init for this class
        pass

    def test_equal(self):
        "Test assertEqual"
        expect = 1
        result = 1
        self.assertEqual(expect, result)

    def test_exception(self):
        "Test assertException"
        self.assertRaises(Exception, fail_function, 0)
#
# main
#
if __name__ == '__main__':
    unittest.main()
