bl_info = {
    "name": "Referencer",
    "author": "alisahanyalcin",
    "version": (1, 1),
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


class Referencer_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text='Reference Images Download Path:')
        row = layout.row()
        home_dir = os.path.expanduser("~")
        documents_dir = os.path.join(home_dir, "Documents")
        row.prop(context.scene, 'Path')

        if not os.path.exists(f"{documents_dir}/referencer"):
            os.makedirs(os.path.join(documents_dir, "referencer"), exist_ok=True)

        row = layout.row()
        row.label(text=f'by default: {documents_dir}\\referencer')


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
        row.prop(scn, 'Image_Url')

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

        row = layout.row()
        row.operator('object.creator', text='Create', icon='IMAGE_PLANE')
        layout.separator()


class Creator(bpy.types.Operator):
    bl_idname = "object.creator"
    bl_label = "Creator"

    def execute(self, context):
        home_dir = os.path.expanduser("~")

        if bpy.context.scene.Path != "":
            documents_dir = bpy.context.scene.Path
        else:
            documents_dir = os.path.join(home_dir, "Documents")

        if not os.path.exists(f"{documents_dir}/referencer"):
            os.makedirs(os.path.join(documents_dir, "referencer"), exist_ok=True)
        else:
            url = bpy.context.scene.Image_Url
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
    bpy.types.Scene.Front = BoolProperty(name="Front", description="to add Front reference image", default=True)
    bpy.types.Scene.Back = BoolProperty(name="Back", description="to add Back reference image", default=True)
    bpy.types.Scene.Left = BoolProperty(name="Left", description="to add Left reference image", default=True)
    bpy.types.Scene.Right = BoolProperty(name="Right", description="to add Right reference image", default=True)
    bpy.types.Scene.Up = BoolProperty(name="Up", description="to add Up reference image", default=True)
    bpy.types.Scene.Down = BoolProperty(name="Down", description="to add Down reference image", default=True)

    bpy.types.Scene.Image_Url = StringProperty(name="", description="Reference Image Url")
    bpy.types.Scene.Path = StringProperty(subtype="FILE_PATH", description="Reference Images Download Path")

    bpy.utils.register_class(Referencer_Preferences)
    bpy.utils.register_class(Referencer_Panel)
    bpy.utils.register_class(Creator)


def unregister():
    bpy.utils.unregister_class(Referencer_Preferences)
    bpy.utils.unregister_class(Referencer_Panel)
    bpy.utils.unregister_class(Creator)


if __name__ == "__main__":
    register()
