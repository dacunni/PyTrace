#!/usr/bin/env python

import Image

from math import sqrt
from math import log

from RayUtils import *
from RenderArtifacts import *
from Sphere import *
from Plane import *

# Definitions



class RadianceSample:
    direction = None
    radiance = 0.0
    def __init__( self, direction, radiance ):
        self.direction = direction
        self.radiance = radiance

class PointLight:
    position = None
    power = 1.0
    def __init__( self, position, power ):
        self.position = position
        self.power = power
    def sample( self, isect ):
        return RadianceSample( self.position.subtract(isect.position).normalize(), self.power )


def shadeIntersection( isect, light ):
    radiance_sample = light.sample( isect )
    # TEMP - This only corrects for the Lambertian dependence on the angle from the normal.
    #        We also need to evaluate the reflectance function
    return radiance_sample.direction.dot( isect.normal ) * radiance_sample.radiance

def shadeIntersectionMulti( isect, lights ):
    value = 0.0
    for light in lights:
        value = value + shadeIntersection( isect, light )
    return value

########

def findClosestIntersection( ray, scene ):
    isect = None

    for obj in scene:
        candidate = obj.intersectRay(ray)
        if candidate is not None:
            fudge = 0.01
            if isect is None:
                isect = candidate
            elif candidate.distance < isect.distance and candidate.distance < fudge:
                isect = candidate
    if isect is not None:
        # Make sure we use the normal that is pointing toward the traced ray
        if isect.normal.dot(r.direction) > 0.0:
            isect.normal = isect.normal.negate()
        isect.position = origin.add(dir.scale(isect.distance))
        isect.origin_ray = ray
        isect.mirror_ray = Ray( isect.position, 
                                ray.direction.negate().add(isect.normal.scale(2.0 * ray.direction.negate().dot(isect.normal))),
                                isect.origin_ray.depth + 1 )
    return isect

def traceRay( ray, scene ):
    radiance = 0.0
    if ray.depth > max_depth:
        return None
    # Find closest intersection with objects in the scene
    isect = findClosestIntersection( ray, scene )
    if isect is not None:
        diffuse_coef = 0.5
        specular_coef = 0.5
        # Calculate local illumination
        isect.radiance_to_origin = diffuse_coef * shadeIntersectionMulti( isect, lights )
        mirror_isect = traceRay( isect.mirror_ray, scene )
        if mirror_isect is not None:
            isect.radiance_to_origin += specular_coef * mirror_isect.radiance_to_origin
    return isect

# ----------------------------------------------------------------------
#                           MAIN
# ----------------------------------------------------------------------

print "Ray Tracer"

width = 256
height = 256
max_depth = 2


artifacts = RenderArtifacts()

artifacts.createNewOutputImages( width, height )

# Load scene file
#execfile("scenes/default.scene"); 
execfile("scenes/grid_spheres.scene"); 

for x in range(width):
    for y in range(height):
        # Create eye ray through pixel (x,y)
        origin = Point(0.0, 0.0, 0.0)
        dir = Vector(float(x) / float(width) - 0.5, 
                     -(float(y) / float(height) - 0.5), 
                     -1.0).normalize()
        r = Ray( origin, dir, 0 )

        # Find the radiance along the ray through pixel (x,y)
        isect = traceRay( r, scene )

        if isect is not None:
            artifacts.updateOutputImages( x, y, isect )

artifacts.saveOutputImages()





