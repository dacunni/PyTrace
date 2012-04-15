#!/usr/bin/env python

from math import sqrt
from math import log

class Vector:
    x = 0.0
    y = 0.0
    z = 0.0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return "<%.3f %.3f %.3f>" % (self.x, self.y, self.z)
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z
    def cross(self, v):
        return Vector( self.y * v.z - self.z * v.y,
                       self.z * v.x - self.x * v.z,
                       self.x * v.y - self.y * v.x )
    def add(self, v):
        return Vector( self.x + v.x,
                       self.y + v.y,
                       self.z + v.z )
    def subtract(self, v):
        return self.add(v.negate())
    def negate(self):
        return Vector( -self.x, 
                       -self.y, 
                       -self.z )
    def scale(self, s):
        return Vector( s * self.x, 
                       s * self.y, 
                       s * self.z )
    def magnitude(self):
        return sqrt( self.dot(self) ) 
    def normalize(self):
        m = self.magnitude()
        if( m == 0.0 ):
            return Vector( 0.0, 0.0, 0.0 )
        else:
            return self.scale( 1.0 / m )

class Point(Vector):
    def __str__(self):
        return "[%.3f %.3f %.3f]" % (self.x, self.y, self.z)

class Ray:
    origin = Point(0.0, 0.0, 0.0)
    direction = Vector(0.0, 0.0, 0.0)
    depth = 0
    def __init__(self, origin, direction, depth):
        self.origin = origin
        self.direction = direction.normalize()
        self.depth = depth
    def __str__(self):
        return "Ra(%s, %s, %d)" % (self.origin, self.direction, self.depth)

class Intersection:
    object = None
    distance = 0.0
    normal = Vector(0.0, 0.0, 0.0)
    position = None
    origin_ray = None
    mirror_ray = None
    radiance_to_origin = None
    def __init__(self, o, d, n):
        self.object = o
        self.distance = d
        self.normal = n
    def __str__(self):
        return "Int(%s, %s, N=%s)" % (self.object, self.distance, self.normal)


