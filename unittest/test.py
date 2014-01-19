from ctypes import * 
 
class _point(Structure): 
    pass 
_point._fields_ = [ 
    ('x', c_int), 
    ('y', c_int), 
] 
point = _point 
class _rect(Structure): 
    pass 
_rect._fields_ = [ 
    ('a', point), 
    ('b', point), 
] 
rect = _rect 
__all__ = ['_rect', '_point', 'rect', 'point']
