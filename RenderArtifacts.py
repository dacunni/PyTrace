
import Image

from RayUtils import *

class RenderArtifacts:

    def __init__(self):
        self.im_render = None
        self.im_intersect_mask = None
        self.im_depth = None
        self.im_normals = None

    def createNewOutputImages( self, width, height ):
        self.im_render = Image.new("RGB", (width, height), (4, 0, 0))
        self.im_intersect_mask = Image.new("RGB", (width, height), (0, 0, 0))
        self.im_depth = Image.new("RGB", (width, height), (0, 0, 0))
        self.im_normals = Image.new("RGB", (width, height), (0, 0, 0))


    def updateOutputImages( self, x, y, isect ):
        value = 0.0
        depth_scaled = 0.0
        radiance = isect.radiance_to_origin

        if isect is not None:
            self.im_intersect_mask.putpixel( (x, y), (255, 255, 255) )
            value = 1.0
            depth_scaled = log(isect.distance) / 5.0

        self.im_render.putpixel((x,y),(int(255.0 * radiance), int(255.0 * radiance), int(255.0 * radiance)))

        depth_scaled = int(depth_scaled * 255.0)
        self.im_depth.putpixel((x,y),(depth_scaled, depth_scaled, depth_scaled))

        if isect is not None:
            self.im_normals.putpixel((x,y),(int((isect.normal.x * 0.5 + 0.5) * 255.0), 
                                       int((isect.normal.y * 0.5 + 0.5) * 255.0),
                                       int((isect.normal.z * 0.5 + 0.5) * 255.0)))
        else:
            self.im_normals.putpixel((x,y),(128,128,255))

    def saveOutputImages( self ):
        self.im_render.save("output/render.png");
        self.im_intersect_mask.save("output/isect.png");
        self.im_depth.save("output/depth.png");
        self.im_normals.save("output/normals.png");

