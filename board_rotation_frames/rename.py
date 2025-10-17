import os

# --- SETTINGS ---
folder = r"C:\Users\danny\Desktop\Super-Sk8!\v2\board_rotation_frames"  # <- change this
flip_step = 10
flip_limit = 350
shuv_step = 10
shuv_limit = 170

# --- RENAME LOGIC ---
frame_index = 0

for shuv_angle in range(0, shuv_limit + shuv_step, shuv_step):
    for flip_angle in range(0, flip_limit + flip_step, flip_step):
        old_name = f"frame{frame_index:04d}.png"
        new_name = f"flip{flip_angle}_shuv{shuv_angle}.png"

        old_path = os.path.join(folder, old_name)
        new_path = os.path.join(folder, new_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"✅ Renamed {old_name} → {new_name}")
        else:
            print(f"⚠️ Missing: {old_name}")

        frame_index += 1

print("🎯 Done renaming all frames!")
