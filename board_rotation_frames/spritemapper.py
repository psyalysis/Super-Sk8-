import os
from PIL import Image

tricks = {
    "BS-Shuv": [0, 180],
    "FS-Shuv": [0, -180],
    "Kickflip": [360, 0],
    "Heelflip": [-360, 0],
    "Varial Kickflip": [360, 180],
    "Varial Heelflip": [-360, 180],
    "Inward Heelflip": [360, -180],
    "Hardflip": [-360, -180],
    "Tre flip": [360, 360],
    "Lazer flip": [-360, -360],
    "360 Hardflip": [360, -360],
    "360 Inward Heelflip": [-360, 360],
}

def create_sprite_map(trick_name, flip_total, shuv_total, frame_step=10, total_frames=18):
    """
    Create a sprite map for a trick animation.
    
    Args:
        trick_name: Name of the trick (e.g., "BS-Shuv")
        flip_total: Total flip rotation (360 = full flip, 0 = no flip)
        shuv_total: Total shuv rotation (180 = half rotation, -180 = reverse)
        frame_step: Step size between frames (default 10 degrees)
        total_frames: Fixed number of frames for all animations (default 18)
    """
    folder = r"C:\Users\danny\Desktop\Super-Sk8!\v2\board_rotation_frames"
    
    sprite_frames = []
    
    for frame in range(total_frames):
        # Calculate progress based on 18-frame system
        progress = frame / (total_frames - 1) if total_frames > 1 else 0
        
        # Calculate current rotation values and ensure they're in 10-degree increments
        if flip_total != 0:
            # For 360-degree shuvs, we need to invert flip direction halfway through
            if abs(shuv_total) == 360:
                # Calculate flip progress normally
                flip_steps = int(abs(flip_total) / 10)
                current_flip_step = int(flip_steps * progress)
                current_flip = current_flip_step * 10
                
                # Invert flip direction halfway through (when shuv reaches 180°)
                if progress >= 0.5:
                    current_flip = flip_total - current_flip
                
                if flip_total < 0:
                    current_flip = -current_flip
            else:
                # Normal calculation for other flip values
                flip_steps = int(abs(flip_total) / 10)
                # Ensure we reach the final step for complete rotation
                current_flip_step = min(int(flip_steps * progress), flip_steps)
                current_flip = (current_flip_step * 10) - 1
                if flip_total < 0:
                    current_flip = -current_flip
        else:
            current_flip = 0
            
        if shuv_total != 0:
            # For 360-degree shuvs, map to available 0-170° range
            if abs(shuv_total) == 360:
                # Calculate smooth 360° rotation using 18 steps with 20° increments
                total_steps = 17  # Total steps for 360° rotation
                current_step = int(total_steps * progress)
                
                # Use 20° steps to complete 360°: 0°, 20°, 40°, ..., 340°
                current_shuv = current_step * 20
                
                # Map to available range (0-170°) by cycling
                if shuv_total < 0:
                    # For negative 360° shuvs, create smooth backward rotation
                    current_shuv = -current_shuv
                    # Map to available range: -0°, -20°, -40°, ..., -160°, -0°, -20°, ...
                    current_shuv = current_shuv % 180
                    if current_shuv > 0:
                        current_shuv = current_shuv - 180  # Convert to negative range
                else:
                    # For positive 360° shuvs, normal cycling
                    current_shuv = current_shuv % 180  # 0°, 20°, 40°, ..., 160°, 0°, 20°, ...
            else:
                # Normal calculation for other shuv values
                shuv_steps = int(abs(shuv_total) / 10)
                current_shuv_step = int(shuv_steps * progress)
                
                if shuv_total < 0:
                    # For negative shuvs, limit to available range (0-170°)
                    # Instead of going to -180°, go to -170° max
                    max_negative_step = min(current_shuv_step, 17)  # Limit to 17 steps (170°)
                    current_shuv = -max_negative_step * 10
                else:
                    # For positive shuvs, limit to available range (0-170°)
                    # Instead of going to 180°, go to 170° max
                    max_positive_step = min(current_shuv_step, 17)  # Limit to 17 steps (170°)
                    current_shuv = max_positive_step * 10
        else:
            current_shuv = 0
        
        # Handle negative rotations by going backwards through available frames
        if current_flip < 0:
            # For negative flip, go backwards: 350, 340, 330, etc.
            flip_for_file = 360 + current_flip
        else:
            # Normalize flip rotation (360 = 0 for file naming)
            flip_for_file = current_flip % 360 if current_flip != 0 else 0
        
        if current_shuv < 0:
            # For negative shuv, map to positive range: -10° -> 170°, -20° -> 160°, etc.
            shuv_for_file = 180 + current_shuv
        else:
            shuv_for_file = current_shuv
        
        # Find the corresponding image file
        filename = f"flip{flip_for_file}_shuv{shuv_for_file}.png"
        filepath = os.path.join(folder, filename)
        
        if os.path.exists(filepath):
            sprite_frames.append(filepath)
            print(f"✅ Found frame {frame}: {filename} (flip={current_flip}°, shuv={current_shuv}°)")
        else:
            print(f"⚠️ Missing frame {frame}: {filename} (flip={current_flip}°, shuv={current_shuv}°)")
    
    # Create sprite map if we have frames
    if sprite_frames:
        create_horizontal_sprite_map(trick_name, sprite_frames)
    else:
        print(f"❌ No frames found for {trick_name}")

def create_horizontal_sprite_map(trick_name, frame_paths):
    """Create a horizontal sprite map by combining frames side by side."""
    if not frame_paths:
        return
    
    # Load all images
    images = []
    for path in frame_paths:
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            return
    
    if not images:
        return
    
    # Get dimensions (assuming all images are the same size)
    width, height = images[0].size
    
    # Create horizontal sprite map
    sprite_map_width = width * len(images)
    sprite_map_height = height
    
    sprite_map = Image.new('RGBA', (sprite_map_width, sprite_map_height))
    
    # Paste images side by side
    for i, img in enumerate(images):
        sprite_map.paste(img, (i * width, 0))
    
    # Save sprite map
    output_path = os.path.join(r"C:\Users\danny\Desktop\Super-Sk8!\v2\animations", f"{trick_name}.png")
    sprite_map.save(output_path)
    print(f"🎯 Created sprite map: {trick_name}.png ({len(images)} frames)")

# Generate sprite maps for all tricks
print("🎬 Creating sprite maps for all tricks...")
for trick_name, (flip_total, shuv_total) in tricks.items():
    print(f"\n📋 Processing {trick_name}: flip={flip_total}°, shuv={shuv_total}°")
    create_sprite_map(trick_name, flip_total, shuv_total)

print("\n✅ All sprite maps created!")