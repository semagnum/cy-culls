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
