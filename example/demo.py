#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Notice: When update demo.py: 
    1. Update README.md
    2. @diyer22 update the answer on stackexchange:
            https://blender.stackexchange.com/a/162746/86396 
"""

import bpy
import bpycv
import random
import numpy as np
from skimage.io import imsave

# remove all MESH objects
[bpy.data.objects.remove(obj) for obj in bpy.data.objects if obj.type == "MESH"]

for index in range(1, 20):
    # create cube and sphere as instance at random location
    location = [random.random() * 4 - 2 for _ in range(3)]
    if index % 2:
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=location)
        categories_id = 1
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=location)
        categories_id = 2
    obj = bpy.context.active_object
    # set each instance a unique inst_id, which is used to generate instance annotation.
    obj["inst_id"] = categories_id * 1000 + index

# render image, instance annoatation and depth in one line code
# result["ycb_meta"] is 6d pose GT
result = bpycv.render_data()

# save result
imsave("demo-rgb.jpg", result["image"])
imsave("demo-inst.png", np.uint16(result["inst"]))  # save instance map as 16 bit png

# convert depth units from meters to millimeters
depth_in_mm = result["depth"] * 1000
imsave("demo-depth.png", np.uint16(depth_in_mm))  # save as 16bit png

# visualization inst_rgb_depth for human
imsave("demo-vis(inst_rgb_depth).jpg", result.vis())
