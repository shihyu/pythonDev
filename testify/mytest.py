#!/usr/bin/env python
# -*- coding: utf-8 -*-

import testify
from ctypes import*
from test import*  # 加载test.py

class Myclass(testify.TestCase):
    def setUp(self):
        self.mylib = CDLL("./libtest.so")
        self.area = self.mylib.area
        print 'setUp'
        pass

    def tearDown(self):
        print 'tearDown'
        pass

    def test1(self):
        print 'test1'
        rc = rect(point(0, 0), point(1, 1))
        self.assert_(self.area(rc) == 1)

if __name__ == "__main__":
    run()
