bl_info = {
    "name": "Referencer",
    "author": "alisahanyalcin",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "3D_Viewport window > N-Panel > Referencer",
    "description": "Add reference images to your scene by url",
    "warning": "To use the Referencer, you need active the 'Import-Export: Import Images as Planes' add-on.",
    "doc_url": "https://github.com/alisahanyalcin/Blender-Referencer",
    "category": "Referencer",
}

import bpy
from bpy.props import *
import urllib
from urllib import request
from urllib.request import Request, urlopen
import uuid
import os


class Referencer_Panel(bpy.types.Panel):
    bl_label = "Referencer"
    bl_idname = "Referencer_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Referencer'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = layout.box()
        row = box.row()

        row.label(text="Reference Image Url")
        row = box.row()
        row.prop(scn, 'MyString')

        box = layout.box()
        row = box.row()
        row.label(text="Plane Sides")
        row = box.row()
        row.prop(scn, 'Front')
        row = box.row()
        row.prop(scn, 'Back')
        row = box.row()
        row.prop(scn, 'Left')
        row = box.row()
        row.prop(scn, 'Right')
        row = box.row()
        row.prop(scn, 'Up')
        row = box.row()
        row.prop(scn, 'Down')

        layout.operator("idname_must.be_all_lowercase_and_contain_one_dot")

        row = layout.row()
        row.operator('object.creator', text='Create', icon='IMAGE_PLANE')
        layout.separator()


class Creator(bpy.types.Operator):
    bl_idname = "object.creator"
    bl_label = "Creator"

    def execute(self, context):
        home_dir = os.path.expanduser("~")
        documents_dir = os.path.join(home_dir, "Documents")

        if not os.path.exists(f"{documents_dir}/referencer"):
            os.makedirs(os.path.join(documents_dir, "referencer"), exist_ok=True)
        else:
            url = bpy.context.scene.MyString
            uid = uuid.uuid1()
            fileExtension = os.path.splitext(f'{url}')[1]

            file = open(f'{documents_dir}/referencer/{uid}{fileExtension}', 'wb')
            request_site = Request(f'{url}', headers={"User-Agent": "Mozilla/5.0"})
            file.write(urllib.request.urlopen(request_site).read())
            file.close()

            if context.scene.Front:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='Y-', relative=False)
                bpy.context.active_object.name = "Front"

            if context.scene.Back:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='Y+', relative=False)
                bpy.context.active_object.name = "Back"

            if context.scene.Left:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='X-', relative=False)
                bpy.context.active_object.name = "Left"

            if context.scene.Right:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='X+', relative=False)
                bpy.context.active_object.name = "Right"

            if context.scene.Up:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='Z-', relative=False)
                bpy.context.active_object.name = "Up"

            if context.scene.Down:
                bpy.ops.import_image.to_plane(files=[{"name": f"{uid}{fileExtension}"}],
                                              directory=f"{documents_dir}/referencer", align_axis='Z+', relative=False)
                bpy.context.active_object.name = "Down"

        return {'FINISHED'}


def register():
    bpy.types.Scene.Front = BoolProperty(name="Front", description="True or False?", default=True)
    bpy.types.Scene.Back = BoolProperty(name="Back", description="True or False?", default=True)
    bpy.types.Scene.Left = BoolProperty(name="Left", description="True or False?", default=True)
    bpy.types.Scene.Right = BoolProperty(name="Right", description="True or False?", default=True)
    bpy.types.Scene.Up = BoolProperty(name="Up", description="True or False?", default=True)
    bpy.types.Scene.Down = BoolProperty(name="Down", description="True or False?", default=True)

    bpy.types.Scene.MyString = StringProperty(name="")

    bpy.utils.register_class(Referencer_Panel)
    bpy.utils.register_class(Creator)


def unregister():
    bpy.utils.unregister_class(Referencer_Panel)
    bpy.utils.unregister_class(Creator)


if __name__ == "__main__":
    register()
