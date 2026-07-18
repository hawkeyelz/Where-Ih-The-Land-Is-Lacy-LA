import pygame
import sys
import os
import random

class LockpickGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.success = False
        self.pickoffset_x = -600
        self.pickoffset_y = 10
        self.bg_img = None
        self.pin_img = None
        self.pick_img = None
        


        # --- NEW: PICK ROTATION CONFIGURATION ---
        self.pick_angle = 0.0       # Current tracking angle
        self.pick_max_angle = 12.0  # Maximum degrees the pick can tilt upward
        self.pick_rot_speed = 2.5   # How fast the pick tilts per frame
        self.pick_return_speed = 3.0 # How fast it snaps back when you let go
        
        # --- PATH & ASSET CONFIGURATION ---
        self.assets_dir = os.path.join("assets", "lockpick")
        
        try:
            # Load and optimize images for the GPU pipeline
            self.bg_img = pygame.image.load(os.path.join(self.assets_dir, "lock_body.png")).convert_alpha()
            self.pin_img = pygame.image.load(os.path.join(self.assets_dir, "pin.png")).convert_alpha()
            self.pick_img = pygame.image.load(os.path.join(self.assets_dir, "pick.png")).convert_alpha()
            
            # Ensure the background fits your 800x600 arcade frame
            self.bg_img = pygame.transform.scale(self.bg_img, (800, 600))
        except Exception as e:  # <--- Changed from pygame.error to Exception
            print(f"Warning: Asset loading failed, falling back to primitive shapes. Error: {e}")
            
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 28, bold=True)
            
        # Minigame parameters
        self.num_pins = 4
        self.pins = []
        self.shear_line = 150
        
        for i in range(self.num_pins):
            self.pins.append({
                "x": 200 + (i * 120),
                "height": 0.0,
                "target": random.randint(120, 180),
                "tolerance": 12,
                "locked": False,
                "velocity": 0.0
            })
            
        self.pick_x = 150
        self.active_pin_idx = 0
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key == pygame.K_LEFT:
                    self.active_pin_idx = max(0, self.active_pin_idx - 1)
                if event.key == pygame.K_RIGHT:
                    self.active_pin_idx = min(self.num_pins - 1, self.active_pin_idx + 1)

        target_x = self.pins[self.active_pin_idx]["x"] + self.pickoffset_x
        self.pick_x += (target_x - self.pick_x) * 0.2
        
        # Lift active pin using UP arrow & handle torque rotation
        active_pin = self.pins[self.active_pin_idx]
        if keys[pygame.K_UP] and not active_pin["locked"]:
            # Rotate pick upward up to our maximum angle limit
            self.pick_angle += self.pick_rot_speed
            if self.pick_angle > self.pick_max_angle:
                self.pick_angle = self.pick_max_angle

            active_pin["height"] += 4.0
            if active_pin["height"] > 250:
                active_pin["height"] = 250
        else:
            # Drop pick back down smoothly to 0 degrees when letting go
            self.pick_angle -= self.pick_return_speed
            if self.pick_angle < 0.0:
                self.pick_angle = 0.0

            # Gravity pulls pin down if not locked
            if not active_pin["locked"]:
                active_pin["height"] -= 5.0
                if active_pin["height"] < 0:
                    active_pin["height"] = 0
                    
        if keys[pygame.K_SPACE]:
            dist = abs(active_pin["height"] - active_pin["target"])
            if dist <= active_pin["tolerance"] and not active_pin["locked"]:
                active_pin["locked"] = True
                active_pin["height"] = active_pin["target"]

    def update(self):
        all_locked = all(pin["locked"] for pin in self.pins)
        if all_locked:
            self.success = True
            self.running = False
### Daw Function 
    ### Daw Function 
    def draw(self):
        # =========================================================================
        # LAYER 1: BACKDROP / BACK WALL (Drawn first at the very bottom)
        # =========================================================================
        # Fill with dark gray background first
        self.screen.fill((40, 44, 52))
            
        # =========================================================================
        # LAYER 2: INTERNAL MECHANICS & TUMBLERS (Pins slide here)
        # =========================================================================
        for idx, pin in enumerate(self.pins):
            # Target range visual track
            target_rect = pygame.Rect(pin["x"] - 15, 300 - pin["target"] - pin["tolerance"], 30, pin["tolerance"] * 2)
            pygame.draw.rect(self.screen, (97, 175, 239, 100), target_rect)
            
            # Channel guidelines
            pygame.draw.rect(self.screen, (75, 82, 99), (pin["x"] - 20, 50, 40, 250), 2)
            
            pin_y = 300 - pin["height"]
            
            # Draw the pin graphics
            if self.pin_img:
                scaled_pin = pygame.transform.scale(self.pin_img, (30, 340))
                self.screen.blit(scaled_pin, (pin["x"] - 15, pin_y - 340))
            else:
                pin_color = (152, 195, 121) if pin["locked"] else (209, 154, 102)
                pygame.draw.rect(self.screen, pin_color, (pin["x"] - 15, pin_y - 80, 30, 80))
            
            # Active Pin indicator dot
            if idx == self.active_pin_idx:
                pygame.draw.circle(self.screen, (229, 192, 123), (pin["x"], pin_y + 10), 6)

        # =========================================================================
        # LAYER 3: FOREGROUND LOCK FACEPLATE (Drawn OVER the sliding pins)
        # =========================================================================
        if self.bg_img:
            # Your front plate with holes masks the pins now!
            self.screen.blit(self.bg_img, (0, 0))

        # =========================================================================
        # LAYER 4: TOOLS & TEXT OVERLAYS (Drawn on top of everything)
        # =========================================================================
        # --- THE LOCKPICK (With Rotation) ---
        pick_y = 315 + self.pickoffset_y
        if self.pick_img:
            # 1. Scale to your exact asset size requirements
            scaled_pick = pygame.transform.scale(self.pick_img, (606, 126))
            
            # 2. Apply the dynamic rotation tracking angle from input physics
            rotated_pick = pygame.transform.rotate(scaled_pick, self.pick_angle)
            
            # 3. Anchor center midpoint coordinates so it spins cleanly without wobbling
            pick_center_x = int(self.pick_x) - 10 + (606 // 2)
            pick_center_y = pick_y - 15 + (126 // 2)
            
            # 4. Correct the bounding box destination tracking 
            rot_rect = rotated_pick.get_rect(center=(pick_center_x, pick_center_y))
            
            # 5. Render onto the viewport canvas
            self.screen.blit(rotated_pick, rot_rect.topleft)
        else:
            # Fallback vector line shapes
            pygame.draw.polygon(self.screen, (171, 178, 191), [
                (self.pick_x, pick_y),
                (self.pick_x + 30, pick_y - 15),
                (self.pick_x + 5, pick_y - 25),
                (self.pick_x - 10, pick_y)
            ])
            pygame.draw.line(self.screen, (171, 178, 191), (0, pick_y), (self.pick_x, pick_y), 8)

        # --- TEXT & HUD INTERFACE ---
        title = self.title_font.render("LOCKPICKING TUMBLERS", True, (230, 192, 123))
        instructions = self.font.render("Arrows to align pick | Hold UP to push pin | SPACE to Lock/Set Pin | ESC to exit", True, (171, 178, 191))
        self.screen.blit(title, (50, 30))
        self.screen.blit(instructions, (50, 80))
        
        # --- TARGET SHEAR LINE ---
        pygame.draw.line(self.screen, (224, 108, 117), (100, 300 - self.shear_line), (700, 300 - self.shear_line), 3)
        shear_lbl = self.font.render("Shear Line", True, (224, 108, 117))
        self.screen.blit(shear_lbl, (710, 285 - self.shear_line))

        pygame.display.flip()
### Run Fuction
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.draw()
            self.bg_img
            
        return self.success

# ==========================================
# --- NEW: STANDALONE TEST RUNNER HARNESS ---
# ==========================================
if __name__ == "__main__":
    pygame.init()
    
    # Generate an isolated 800x600 runtime canvas
    test_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lacy La Minigame Test Environment")
    
    # Fire up the minigame completely separated from main.py
    game = LockpickGame(test_screen)
    print("Launching isolated lockpick testing engine...")
    outcome = game.run()
    
    print(f"Sandbox closed! Returned outcome to engine context: {outcome}")
    pygame.quit()
    sys.exit()