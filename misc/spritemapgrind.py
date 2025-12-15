import os
from PIL import Image

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Frame dimensions
FRAME_WIDTH = 96
FRAME_HEIGHT = 96
NUM_FRAMES = 13  # grind_0000.png through grind_0012.png

def create_spritemap(folder_path, folder_name):
    """Create a spritemap from all frames in a folder."""
    frames = []
    
    # Load all frames
    for i in range(NUM_FRAMES):
        frame_path = os.path.join(folder_path, f"grind_{i:04d}.png")
        if os.path.exists(frame_path):
            frames.append(Image.open(frame_path))
        else:
            print(f"Warning: Frame {i} not found in {folder_name}")
    
    if not frames:
        print(f"No frames found in {folder_name}")
        return
    
    # Create spritemap: 13 frames horizontally
    spritemap_width = len(frames) * FRAME_WIDTH
    spritemap_height = FRAME_HEIGHT
    spritemap = Image.new('RGBA', (spritemap_width, spritemap_height))
    
    # Paste frames into spritemap
    for i, frame in enumerate(frames):
        x_offset = i * FRAME_WIDTH
        spritemap.paste(frame, (x_offset, 0))
    
    # Save spritemap
    output_path = os.path.join(script_dir, f"{folder_name}.png")
    spritemap.save(output_path)
    print(f"Created: {output_path}")

def main():
    """Process all grind animation folders."""
    # Get all items in the grindFrames directory
    items = os.listdir(script_dir)
    
    for item in items:
        item_path = os.path.join(script_dir, item)
        
        # Only process directories (skip this script file)
        if os.path.isdir(item_path):
            print(f"Processing: {item}")
            create_spritemap(item_path, item)
    
    print("All spritemaps created!")

if __name__ == "__main__":
    main()

