import bpy, bgl, blf, sys
from bpy import data, ops, props, types, context
import math
import random
from mathutils import Vector


def add_cameras(cam_name, obj_name, n):
    """
    Adds 11 additional cameras 30 degrees around an initial camera.
    Preprocessing for MVCNN: http://vis-www.cs.umass.edu/mvcnn/docs/su15mvcnn.pdf
    Credit: https://blender.stackexchange.com/questions/176296/add-camera-at-random-position-through-python
    """
    camera = bpy.data.objects[cam_name]  # Make sure your first camera is named 'MainCamera'
    target_object = bpy.data.objects[obj_name]  # The camera will face this object. /!\ Naming

    z = camera.location[2]
    radius = Vector((camera.location[0], camera.location[1], 0)).length

    interval = 1 / n
    print(interval)
    for i in range(1, n + 1):
        print(i)
        angle = 2 * math.pi * (i * interval)

        # Randomly place the camera on a circle around the object at the same height as the main camera
        new_camera_pos = Vector((radius * math.cos(angle), radius * math.sin(angle), z))

        bpy.ops.object.camera_add(enter_editmode=False, location=new_camera_pos)

        # Add a new track to constraint and set it to track your object
        track_to = bpy.context.object.constraints.new('TRACK_TO')
        track_to.target = target_object
        track_to.track_axis = 'TRACK_NEGATIVE_Z'
        track_to.up_axis = 'UP_Y'

        # Set the new camera as active
        bpy.context.scene.camera = bpy.context.object


def take_pictures(file_path):
    """
    """
    scene_key = bpy.data.scenes.keys()[0]

    for obj in bpy.data.objects:
        if obj.name.startswith('Camera.'):
            bpy.data.scenes[scene_key].camera = obj
            bpy.context.scene.render.filepath = file_path + obj.name + '.png'
            bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    add_cameras('Camera', 'Sphere', 12)
    take_pictures('test')