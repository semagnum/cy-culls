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
    importlib.reload(panel)
else:
    from . import operators, panel

import bpy

bl_info = {
    'name': 'Cy-Culls',
    'author': 'Spencer Magnusson',
    'version': (0, 0, 2),
    'blender': (2, 92, 0),
    'description': 'Consolidated table to set Cycles culling settings',
    'location': 'Scene',
    'support': 'COMMUNITY',
    'category': 'Render'
}

classes = [operators.SM_OT_Cycull, panel.SM_UL_Cycull, panel.SM_PT_CyCullsTable]
properties = [
    ('sm_cyculls_active_object', bpy.props.IntProperty(default=0))
]


def register():
    window_manager = bpy.types.WindowManager

    for name, prop in properties:
        full_name = name
        setattr(window_manager, full_name, prop)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    window_manager = bpy.types.WindowManager
    for name, prop in properties:
        full_name = name
        delattr(window_manager, full_name)


if __name__ == '__main__':
    register()
