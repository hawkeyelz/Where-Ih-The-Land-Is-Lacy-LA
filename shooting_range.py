import pygame
import sys
import json
import math

class ShootingRangeGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.success = False

        # --- PLAYER GAMEPLAY STATES (Driven by dynamic variables) ---
        self.health = 100.0
        self.money = 1000  # Starting cash balance
        self.max_ammo = 6
        self.current_ammo = 6
        
        # --- TUNABLE GAMEPLAY PERCENTAGES & PENALTIES ---
        self.damage_taken_pct = 20.0       # Health lost when shot by enemy
        self.hostage_cash_penalty_pct = 15.0 # Money lost if you shoot an innocent
        
        # --- VISUAL ASSET INITIALIZER PLACEHOLDERS (Replaceable by PNGs) ---
        self.crosshair_img = None
        self.hud_ammo_img = None
        self.hud_health_img = None
        
        # Initialize Fonts
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 18)
        self.hud_font = pygame.font.SysFont("Arial", 24, bold=True)

        # --- SAMPLE JSON DATA PATTERN ---
        # This mirrors the level structures you'll load from your database
        self.level_data = {
            "scenery": [
                {"type": "building", "x": 50, "y": 150, "width": 300, "height": 350, "color": (100, 100, 105)},
                {"type": "building", "x": 450, "y": 200, "width": 300, "height": 300, "color": (120, 110, 105)},
                {"type": "window", "x": 100, "y": 200, "width": 50, "height": 70, "color": (20, 20, 25)},
                {"type": "window", "x": 220, "y": 200, "width": 50, "height": 70, "color": (20, 20, 25)},
                {"type": "door", "x": 150, "y": 380, "width": 60, "height": 120, "color": (15, 15, 15)},
                {"type": "vehicle", "x": 380, "y": 420, "width": 140, "height": 90, "color": (128, 0, 128)},
                {"type": "dumpster", "x": 80, "y": 440, "width": 90, "height": 60, "color": (0, 0, 255)},
                {"type": "newsstand", "x": 680, "y": 400, "width": 70, "height": 100, "color": (148, 0, 211)}
            ],
            "spawn_points": [
                {"id": "window_1", "x": 100, "y": 200, "type": "window"},
                {"id": "dumpster_left", "x": 180, "y": 440, "type": "side_pop"},
                {"id": "car_rear", "x": 410, "y": 380, "type": "cover"}
            ]
        }

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left Click = Fire Gun
                if event.button == 1:
                    if self.current_ammo > 0:
                        self.current_ammo -= 1
                        self.check_shot(event.pos)
                    else:
                        print("Click! Out of ammo! Right-click to reload.")
                        
                # Right Click = Reload Matrix
                elif event.button == 3:
                    self.current_ammo = self.max_ammo
                    print("Reloaded!")

    def check_shot(self, mouse_pos):
        # Target detection framework will connect here in Step 2
        pass

    def update(self):
        # Health safety cutoff
        if self.health <= 0:
            self.health = 0
            self.running = False
            self.success = False

    def draw(self):
        # Sky background floor paint
        self.screen.fill((135, 206, 235))
        
        # 1. RENDER SCENERY LAYER (Looping through data configurations)
        for item in self.level_data["scenery"]:
            pygame.draw.rect(self.screen, item["color"], (item["x"], item["y"], item["width"], item["height"]))
            # Optional black structural borders for architectural clarity
            pygame.draw.rect(self.screen, (0, 0, 0), (item["x"], item["y"], item["width"], item["height"]), 2)

        # 2. RENDER THE HUD / INTERFACE LAYER
        # Health Bar Drawing Mechanics
        pygame.draw.rect(self.screen, (255, 0, 0), (50, 30, 200, 25))
        health_width = int(200 * (self.health / 100.0))
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 30, health_width, 25))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 30, 200, 25), 2)
        
        # Ammo Count Pip indicators
        for i in range(self.max_ammo):
            color = (255, 215, 0) if i < self.current_ammo else (50, 50, 50)
            pygame.draw.circle(self.screen, color, (300 + (i * 20), 42), 8)
            pygame.draw.circle(self.screen, (0, 0, 0), (300 + (i * 20), 42), 8, 1)

        # Cash Account Text Overlay
        money_text = self.hud_font.render(f"${int(self.money)}", True, (34, 139, 34))
        self.screen.blit(money_text, (500, 28))
        
        # Informational HUD text labels
        lbl_health = self.font.render("HEALTH", True, (0, 0, 0))
        lbl_ammo = self.font.render("AMMO", True, (0, 0, 0))
        self.screen.blit(lbl_health, (50, 10))
        self.screen.blit(lbl_ammo, (300, 10))

        # 3. INTERACTIVE RETICLE CROSSHAIR (Drawn over scenery, under target vectors)
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), (mx, my), 15, 2)
        pygame.draw.line(self.screen, (255, 0, 0), (mx - 20, my), (mx + 20, my), 2)
        pygame.draw.line(self.screen, (255, 0, 0), (mx, my - 20), (mx, my + 20), 2)

        pygame.display.flip()

    def run(self):
        # Hide standard system cursor to let the graphical tracking rect display properly
        pygame.mouse.set_visible(False)
        
        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.draw()
            
        pygame.mouse.set_visible(True)
        return self.success

if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Lacy La Shooting Range Target Sandbox")
    
    game = ShootingRangeGame(test_screen)
    print("Launching shooting gallery architecture test harness...")
    game.run()
    pygame.quit()