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

if "bpy" in locals():
    import importlib
    importlib.reload(operators)
else:
    from . import operators

import bpy


class SM_UL_Cycull(bpy.types.UIList):
    visible_only: bpy.props.BoolProperty(
        name='Visible Only',
        description='Only show visible objects',
        default=True
    )
    selection_only: bpy.props.BoolProperty(
        name='Selected Only',
        description='Only show selected objects',
        default=False
    )

    def draw_item(self, context, layout, data, item_obj, icon, active_data, active_propname, index):
        if not operators.valid_item(item_obj):
            return
        layout.template_icon(icon_value=icon)
        layout.label(text=item_obj.name)
        layout.prop(item_obj.cycles, 'use_camera_cull', icon='CAMERA_DATA', icon_only=True)
        layout.prop(item_obj.cycles, 'use_distance_cull', icon='DRIVER_DISTANCE', icon_only=True)

    def draw_filter(self, context, layout):
        row = layout.row()
        row.prop(self, 'filter_name', text='')
        row.prop(self, 'visible_only', text='', icon='HIDE_OFF')
        row.prop(self, 'selection_only', text='', icon='RESTRICT_SELECT_OFF')

    def filter_items(self, context, data, propname):
        all_objects = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item,
                                                          all_objects, 'name')
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(all_objects)

        for idx, obj in enumerate(all_objects):
            if not operators.valid_item(obj) or (self.visible_only and obj.hide_get()) or (
                    self.selection_only and not obj.select_get()):
                flt_flags[idx] = 0

        return flt_flags, flt_neworder


class SM_PT_CyCullsTable(bpy.types.Panel):
    bl_label = 'Cy-Culls'
    bl_category = 'Cy-Culls'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        def add_operators(sublayout, prop):
            row = sublayout.row()
            enable_all = row.operator(operators.SM_OT_Cycull.bl_idname, text='Enable All', icon='CHECKMARK')
            enable_all.cycles_culling_property = prop
            enable_all.cycles_culling_value = True
            disable_all = row.operator(operators.SM_OT_Cycull.bl_idname, text='Disable All', icon='X')
            disable_all.cycles_culling_property = prop
            disable_all.cycles_culling_value = False

        layout = self.layout
        scene = context.scene
        cscene = scene.cycles
        layout.prop(scene.render, 'use_simplify')
        box = layout.box()
        box.active = scene.render.use_simplify

        row = box.row(heading='Camera Culling')
        row.prop(cscene, 'use_camera_cull', text='')
        sub = row.column()
        sub.active = getattr(cscene, 'use_camera_cull')
        sub.prop(cscene, 'camera_cull_margin', text='')
        add_operators(box, 'use_camera_cull')

        box.separator()

        row = box.row(heading='Distance Culling')
        row.prop(cscene, 'use_distance_cull', text='')
        sub = row.column()
        sub.active = getattr(cscene, 'use_distance_cull')
        sub.prop(cscene, 'distance_cull_margin', text='')
        add_operators(box, 'use_distance_cull')

        layout.template_list('SM_UL_Cycull', '', context.scene, 'objects', context.window_manager, 'sm_cyculls_active_object')
