#!/usr/bin/env python 
# -*- coding: utf-8 -*-
 
import unittest 
from ctypes import * #加载ctypes 
from test import * #加载test.py 
 
class Myclass( unittest.TestCase ): 
    def setUp( self ): 
        print 'setUp'
        pass 
 
    def tearDown( self ): 
        print 'tearDown'
        pass 
 
    def test1( self ): 
        print 'test1'
        rc = rect( point(0, 0), point(1, 1) ) 
        self.assert_( area( rc ) == 1 ) 
 
if __name__ == "__main__": 
    mylib = CDLL( "./libtest.so" ) 
    area = mylib.area 
    unittest.main()
