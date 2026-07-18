import pygame
import sys

class LockpickMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        
        # Game State
        self.running = True
        self.success = False
        
        # Try to load assets, fall back to None if not found
        try:
            self.bg_img = pygame.image.load("assets/lock_background.png").convert()
        except:
            self.bg_img = None
            
        # Minigame parameters
        self.num_pins = 4
        self.pins = [] # List of dicts representing each pin's state
        self.shear_line = 150  # Y coordinate where pins must align to lock in
        
        # Generate target zones for the pins
        # Each pin has a current height, a target sweet-spot, and a status (0 = loose, 1 = locked)
        import random
        for i in range(self.num_pins):
            self.pins.append({
                "x": 200 + (i * 120),
                "height": 0.0,
                "target": random.randint(120, 180),
                "tolerance": 12,
                "locked": False,
                "velocity": 0.0
            })
            
        # Pick tool properties
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
                    self.running = False # Bail out
                
                # Navigate pick tool left and right
                if event.key == pygame.K_LEFT:
                    self.active_pin_idx = max(0, self.active_pin_idx - 1)
                if event.key == pygame.K_RIGHT:
                    self.active_pin_idx = min(self.num_pins - 1, self.active_pin_idx + 1)

        # Smoothly move pick toward active pin
        target_x = self.pins[self.active_pin_idx]["x"] - 10
        self.pick_x += (target_x - self.pick_x) * 0.2
        
        # Lift active pin using UP arrow
        active_pin = self.pins[self.active_pin_idx]
        if keys[pygame.K_UP] and not active_pin["locked"]:
            active_pin["height"] += 4.0
            if active_pin["height"] > 250:
                active_pin["height"] = 250
        else:
            # Gravity pulls pin down if not locked
            if not active_pin["locked"]:
                active_pin["height"] -= 5.0
                if active_pin["height"] < 0:
                    active_pin["height"] = 0
                    
        # Lock check: If player taps SPACE while pin is in the target sweet-spot, lock it!
        if keys[pygame.K_SPACE]:
            dist = abs(active_pin["height"] - active_pin["target"])
            if dist <= active_pin["tolerance"] and not active_pin["locked"]:
                active_pin["locked"] = True
                active_pin["height"] = active_pin["target"] # Snap to target

    def update(self):
        # Check if all pins are locked
        all_locked = all(pin["locked"] for pin in self.pins)
        if all_locked:
            self.success = True
            self.running = False

    def draw(self):
        # Background
        if self.bg_img:
            self.screen.blit(self.bg_img, (0, 0))
        else:
            self.screen.fill((40, 44, 52)) # Slate gray background
            
        # Draw Header
        title = self.title_font.render("LOCKPICKING TUMBLERS", True, (230, 192, 123))
        instructions = self.font.render("Arrows to align pick | Hold UP to push pin | SPACE to Lock/Set Pin | ESC to exit", True, (171, 178, 191))
        self.screen.blit(title, (50, 30))
        self.screen.blit(instructions, (50, 80))
        
        # Draw Shear Line (Target alignment guide)
        pygame.draw.line(self.screen, (224, 108, 117), (100, 300 - self.shear_line), (700, 300 - self.shear_line), 3)
        shear_lbl = self.font.render("Shear Line", True, (224, 108, 117))
        self.screen.blit(shear_lbl, (710, 285 - self.shear_line))
        
        # Draw Pins
        for idx, pin in enumerate(self.pins):
            # Target range visual background box
            target_rect = pygame.Rect(pin["x"] - 15, 300 - pin["target"] - pin["tolerance"], 30, pin["tolerance"] * 2)
            pygame.draw.rect(self.screen, (97, 175, 239, 100), target_rect)
            
            # Draw Pin housing
            pygame.draw.rect(self.screen, (75, 82, 99), (pin["x"] - 20, 50, 40, 250), 2)
            
            # Pin dynamic position
            pin_y = 300 - pin["height"]
            pin_color = (152, 195, 121) if pin["locked"] else (209, 154, 102) # Green if locked, copper if loose
            
            # Draw actual sliding pin
            pygame.draw.rect(self.screen, pin_color, (pin["x"] - 15, pin_y - 80, 30, 80))
            
            # Active Pin highlight ring
            if idx == self.active_pin_idx:
                pygame.draw.circle(self.screen, (229, 192, 123), (pin["x"], pin_y + 10), 6)

        # Draw Pick Tool (represented as a metallic rod sliding below the pins)
        pick_y = 315
        pygame.draw.polygon(self.screen, (171, 178, 191), [
            (self.pick_x, pick_y),
            (self.pick_x + 30, pick_y - 15),
            (self.pick_x + 5, pick_y - 25),
            (self.pick_x - 10, pick_y)
        ])
        pygame.draw.line(self.screen, (171, 178, 191), (0, pick_y), (self.pick_x, pick_y), 8)

        pygame.display.flip()

    def run(self):
        """Standard pygame loop context wrapper."""
        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.draw()
            
        return self.success