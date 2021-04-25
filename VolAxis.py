import bpy, mathutils, os, sys
from bpy import context
# Get file dialogue
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator
# Wave Object
from waveobject import waveObj


scene = bpy.context.scene
obj = context.active_object




class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Select WAV"
    
    filter_glob: StringProperty(
        default='*.wav',
        options={'HIDDEN'}
    )

    def execute(self, context):
        """Do something with the selected file(s)."""

        filename, extension = os.path.splitext(self.filepath)
        print('Name: ', filename)
        audio = waveObj(self.filepath)
        
        min_val = 0
        max_val = 30
        
        frame_num = 1
        while frame_num < audio.length_of_data("frames"):
            scene.frame_set(frame_num)
            obj.location.z = audio.sample_RMS_clamped(audio.sample_at_frame(frame_num), 0.01, min_val, max_val)
            obj.keyframe_insert(data_path="location", index=-1)
            frame_num += 1
        
        #
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)
        
def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)
        
if __name__ == "__main__":
    register()
    
    bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')

