import bpy

from .operators import SM_OT_Cycull
from .panel import SM_UL_Cycull, SM_PT_CyCullsTable

bl_info = {
    'name': 'Cy-Culls',
    'author': 'Spencer Magnusson',
    'version': (0, 0, 1),
    'blender': (2, 92, 0),
    'description': 'Consolidated table to set Cycles culling settings',
    'location': 'Scene',
    'support': 'COMMUNITY',
    'category': 'Render'
}

classes = [SM_OT_Cycull, SM_UL_Cycull, SM_PT_CyCullsTable]
properties = [
    ('sm_cyculls_active_object', bpy.props.IntProperty(default=0))
]


def register():
    scene = bpy.types.Scene

    for name, prop in properties:
        full_name = name
        setattr(scene, full_name, prop)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    scene = bpy.types.Scene
    for name, prop in properties:
        full_name = name
        delattr(scene, full_name)


if __name__ == '__main__':
    register()
