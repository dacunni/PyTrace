#!/usr/bin/env python

import Image

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

u = Vector(2.0, 0.0, 0.0)
v = Vector(0.0, 1.0, 0.0)
p = Point(3.0, 4.0, 5.0)
s = Sphere( Point(0.0, 0.0, -3.0), 0.5 )
r = Ray( Point(0.0, 0.0, 0.0), Vector(0.0, 0.0, -1.0) )
scene = [ 
         Sphere( Point(0.0, 0.0, -3.0), 0.5 ),
         Sphere( Point(1.0, 0.0, -5.0), 0.5 ),
         Sphere( Point(-1.0, 0.0, -2.0), 0.5 ),
         Sphere( Point(0.0, 3.0, -10.0), 0.5 ),
         Sphere( Point(0.0, -1.0, -6.0), 0.5 ),
         Plane( 0.0, 1.0, 0.0, -1.0 ),
         Plane( 1.0, 0.0, 0.0, 2.0 )
        ]
print "u =", u
print "v =", v
print "p =", p
print "s =", s
print "r =", r
print u, "dot", v, "=", u.dot(v)
print u, "cross", v, "=", u.cross(v)
print u, "cross", v, "=", u.cross(v)
print u, "add", v, "=", u.add(v)
print u, "subtract", v, "=", u.subtract(v)
print "magnitude", u, "=", u.magnitude()
print "normalize", u, "=", u.normalize()

print "intersectRay:", s.intersectRay(r)

########

print "Ray Tracer"

width = 256
height = 256

im_render = Image.new("RGB", (width, height), (0, 0, 0))
im_depth = Image.new("RGB", (width, height), (0, 0, 0))
im_normals = Image.new("RGB", (width, height), (0, 0, 0))

for x in range(width):
    for y in range(height):
        value = 0.0
        depth_scaled = 0.0
        isect = None

        origin = Point(0.0, 0.0, 0.0)
        dir = Vector(float(x) / float(width) - 0.5, 
                     float(y) / float(height) - 0.5, 
                     -1.0).normalize()
        r = Ray( origin, dir )

        for obj in scene:
            candidate = obj.intersectRay(r)
            if candidate is not None:
                if isect is None:
                    isect = candidate
                elif candidate.distance < isect.distance:
                    isect = candidate

        if isect is not None:
            value = 1.0
            depth_scaled = isect.distance / 10.0

        im_render.putpixel((x,y),(0, int(255.0 * value), 0))

        depth_scaled = int(depth_scaled * 255.0)
        im_depth.putpixel((x,y),(depth_scaled, depth_scaled, depth_scaled))

        if isect is not None:
            im_normals.putpixel((x,y),(int(isect.normal.x * 255.0), 
                                       int(isect.normal.y * 255.0),
                                       int(isect.normal.z * 255.0)))
        else:
            im_normals.putpixel((x,y),(0, 0, 0))

im_render.save("render.png");
im_depth.save("depth.png");
im_normals.save("normals.png");




