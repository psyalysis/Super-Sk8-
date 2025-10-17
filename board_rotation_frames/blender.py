import bpy
import math

# --- SETTINGS ---
output_path = "C:\\Users\\danny\\Desktop\\Super-Sk8!\\v2\\board_rotation_frames\\"  # Change to your desired output directory
horizontal_step = 20
barrel_step = 20
horizontal_limit = 180
barrel_limit = 360

# Get active object and perform a safety check
obj = bpy.context.active_object
if obj is None:
    print("❌ ERROR: No object is currently selected (active). Please select your board.")
    # Stop the script if no object is selected
    raise Exception("No active object selected.")

# Reset rotation to start from a clean slate
obj.rotation_euler = (0, 0, 0)

# Loop over barrel roll and horizontal rotations
frame = 0
for barrel in range(0, barrel_limit, barrel_step):
    for horiz in range(0, horizontal_limit + horizontal_step, horizontal_step):
        
        # Set rotation: Try different axis combinations
        # Option 1: X-axis barrel roll, Z-axis horizontal (most common)
        obj.rotation_euler = (math.radians(barrel), 0, math.radians(horiz))
        
        # If this doesn't work, try these alternatives by uncommenting one:
        # Option 2: Y-axis barrel roll, Z-axis horizontal
        # obj.rotation_euler = (0, math.radians(barrel), math.radians(horiz))
        
        # Option 3: Z-axis barrel roll, Y-axis horizontal  
        # obj.rotation_euler = (0, math.radians(horiz), math.radians(barrel))
        
        # Option 4: Y-axis barrel roll, X-axis horizontal
        # obj.rotation_euler = (math.radians(horiz), math.radians(barrel), 0)
        
        # Ensure the view layer updates to reflect the new rotation
        bpy.context.view_layer.update()
        
        # Set the unique file path and render the frame
        bpy.context.scene.render.filepath = f"{output_path}{frame:00d}_barrel{barrel}_horiz{horiz}.png"
        bpy.ops.render.render(write_still=True)
        
        frame += 1

print(f"✅ All renders complete. Total frames rendered: {frame}")