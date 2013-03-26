#!/usr/bin/env python

from math import sqrt
from math import log

from RayUtils import *

# Definitions

class Sphere:
    center = Point(0.0, 0.0, 0.0)
    radius = 1.0
    def __init__(self, c, r):
        self.center = c
        self.radius = r
    def __str__(self):
        return "Sph(%s, %.3f)" % (self.center, self.radius)
    def intersectRay(self, ray):
        dst = ray.origin.subtract(self.center)
        B = dst.dot(ray.direction)
        C = dst.dot(dst) - self.radius * self.radius
        D = B * B - C
        if D > 0.0:
            t = -B - sqrt(D)
            return Intersection(self, 
                                t,
                                (ray.origin.add(ray.direction.scale(t))).subtract(self.center).normalize())
        else:
            return None


