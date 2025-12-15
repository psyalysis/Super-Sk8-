import pygame
import os
import glob

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_SIZE = 64 # Each frame is 128x128px
FPS = 16  # Animation speed (frames per second)

class AnimationViewer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Animation Viewer - Press SPACE to cycle animations")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Get all animation files
        self.animation_files = glob.glob("*.png")
        self.current_animation_index = 0
        self.current_animation = None
        self.current_frame = 0
        self.frame_count = 0
        
        # Load the first animation
        self.load_animation()
        
        # Font for text display
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def load_animation(self):
        """Load the current animation sprite map"""
        if not self.animation_files:
            print("No animation files found!")
            return
        
        filename = self.animation_files[self.current_animation_index]
        print(f"Loading: {filename}")
        
        try:
            # Load the sprite map
            sprite_map = pygame.image.load(filename)
            sprite_map = sprite_map.convert_alpha()
            
            # Calculate number of frames (assuming 128px wide per frame)
            self.frame_count = sprite_map.get_width() // FRAME_SIZE
            
            # Extract individual frames
            self.frames = []
            for i in range(self.frame_count):
                frame_rect = pygame.Rect(i * FRAME_SIZE, 0, FRAME_SIZE, FRAME_SIZE)
                frame_surface = pygame.Surface((FRAME_SIZE, FRAME_SIZE), pygame.SRCALPHA)
                frame_surface.blit(sprite_map, (0, 0), frame_rect)
                self.frames.append(frame_surface)
            
            self.current_frame = 0
            print(f"Loaded {self.frame_count} frames")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            self.frames = []
            self.frame_count = 0
    
    def next_animation(self):
        """Cycle to the next animation"""
        self.current_animation_index = (self.current_animation_index + 1) % len(self.animation_files)
        self.load_animation()
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_animation()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update animation frame"""
        if self.frame_count > 0:
            self.current_frame = (self.current_frame + 1) % self.frame_count
    
    def draw(self):
        """Draw the current frame and UI"""
        self.screen.fill((50, 50, 50))  # Dark gray background
        
        if self.frames and self.current_frame < len(self.frames):
            # Draw the current frame centered
            frame = self.frames[self.current_frame]
            frame_rect = frame.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(frame, frame_rect)
            
            # Draw frame border
            pygame.draw.rect(self.screen, (255, 255, 255), frame_rect, 2)
        
        # Draw UI text
        if self.animation_files:
            current_filename = self.animation_files[self.current_animation_index]
            
            # Animation name
            name_text = self.font.render(current_filename, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(name_text, name_rect)
            
            # Frame info
            frame_text = self.small_font.render(f"Frame: {self.current_frame + 1}/{self.frame_count}", True, (200, 200, 200))
            frame_rect = frame_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(frame_text, frame_rect)
            
            # Instructions
            instructions = [
                "SPACE - Next Animation",
                "ESC - Exit"
            ]
            
            for i, instruction in enumerate(instructions):
                inst_text = self.small_font.render(instruction, True, (150, 150, 150))
                inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60 + i * 25))
                self.screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        frame_timer = 0
        
        while self.running:
            dt = self.clock.tick(60)  # 60 FPS for smooth UI
            
            self.handle_events()
            
            # Update animation at specified FPS
            frame_timer += dt
            if frame_timer >= 1000 / FPS:  # Convert FPS to milliseconds
                self.update()
                frame_timer = 0
            
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    # Change to animations directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🎬 Animation Viewer Starting...")
    print("📁 Looking for animation files in:", os.getcwd())
    
    viewer = AnimationViewer()
    viewer.run()
