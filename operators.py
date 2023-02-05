"""
Copyright (C) 2023 Spencer Magnusson
semagnum@gmail.com
Created by Spencer Magnusson
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import bpy


def valid_item(ob):
    return ob.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META', 'LIGHT', 'VOLUME', 'POINTCLOUD', 'HAIR'} or (
            ob.instance_type == 'COLLECTION' and ob.instance_collection)


class SM_OT_Cycull(bpy.types.Operator):
    """Cycle Cull Mode"""
    bl_idname = 'sm.cycull'
    bl_label = 'Apply Cycles Culling Setting to all Objects'
    bl_options = {'REGISTER', 'UNDO'}

    cycles_culling_property: bpy.props.EnumProperty(
        items=[
            ('use_camera_cull', 'Camera culling', ''),
            ('use_distance_cull', 'Distance culling', ''),
        ],
        name='Culling Property',
        default='use_camera_cull'
    )
    cycles_culling_value: bpy.props.BoolProperty()

    def execute(self, context):
        scene = context.scene
        for o in scene.objects:
            if valid_item(o):
                setattr(o.cycles, self.cycles_culling_property, self.cycles_culling_value)
                o.update_tag()
        return {'FINISHED'}
