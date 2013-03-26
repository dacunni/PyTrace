
from math import sqrt
from math import log

from RayUtils import *

# Definitions

class Plane:
    A = 0.0
    B = 0.0
    C = 0.0
    D = 0.0
    def __init__(self, a, b, c, d):
        self.A = a
        self.B = b
        self.C = c
        self.D = d
    def __str__(self):
        return "Pl(%.3f, %.3f, %.3f, %.3f)" % (self.A, self.B, self.C, self.D)
    def intersectRay(self, ray):
        normal = Vector(self.A, self.B, self.C)
        num = -(normal.dot(ray.origin) + self.D)
        den = normal.dot(ray.direction)
        if den == 0.0: 
            return None
        normal = normal.normalize()
        t = num / den
        if t > 0.0:
            return Intersection( self, t, normal )
        else:
            return None

