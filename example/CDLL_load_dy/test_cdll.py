#!/usr/bin/env python 
from ctypes import * 
 
libc = CDLL( "libc.so.6" ) 
printf = libc.printf 
strcpy = libc.strcpy 
s = c_char_p( "Hello, world!" ) 
printf("%s\n", s) 
t = create_string_buffer( 32 ) 
strcpy(t, s) 
printf("%s\n", t)
