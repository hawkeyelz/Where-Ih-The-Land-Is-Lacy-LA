import pygame
import sys
import os
import random

class ShootingRangeGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.success = False

        # --- PLAYER GAMEPLAY STATES ---
        self.health = 100.0
        self.money = 1000
        self.max_ammo = 6
        self.current_ammo = 6
        
        # --- TUNABLE GAMEPLAY VARIABLES ---
        self.damage_taken_pct = 20.0       # Health lost when shot by an enemy
        self.hostage_cash_penalty_pct = 15.0 # Money lost if you shoot an innocent
        
        # Initialize Fonts
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 18)
        self.hud_font = pygame.font.SysFont("Arial", 24, bold=True)

        # --- DYNAMIC ACTIVE TARGET LIST ---
        self.active_targets = []
        self.spawn_timer = 0
        self.spawn_rate = 90  # Frames between new spawns (~1.5 seconds)

        # --- LEVEL DESIGN LAYOUT DATA ---
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
                {"id": "window_left", "x": 105, "y": 205, "width": 40, "height": 60, "slide_dir": "up", "slide_dist": 60},
                {"id": "window_right", "x": 225, "y": 205, "width": 40, "height": 60, "slide_dir": "up", "slide_dist": 60},
                {"id": "dumpster_side", "x": 175, "y": 420, "width": 45, "height": 80, "slide_dir": "left", "slide_dist": 50},
                {"id": "car_top", "x": 430, "y": 350, "width": 45, "height": 80, "slide_dir": "up", "slide_dist": 70},
                {"id": "newsstand_side", "x": 630, "y": 410, "width": 45, "height": 80, "slide_dir": "right", "slide_dist": 50}
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
                if event.button == 1:
                    if self.current_ammo > 0:
                        self.current_ammo -= 1
                        self.check_shot(event.pos)
                    else:
                        print("Click! Out of ammo! Right-click to reload.")
                        
                elif event.button == 3:
                    self.current_ammo = self.max_ammo
                    print("Reloaded!")

    def spawn_target(self):
        point = random.choice(self.level_data["spawn_points"])
        
        if any(t["spawn_id"] == point["id"] for t in self.active_targets):
            return

        roll = random.randint(0, 2)
        
        target = {
            "spawn_id": point["id"],
            "target_x": point["x"],
            "target_y": point["y"],
            "width": point["width"],
            "height": point["height"],
            "slide_dir": point["slide_dir"],
            "slide_dist": point["slide_dist"],
            
            "progress": 0.0,
            "state": "sliding_in",
            "slide_speed": 0.15,
            
            "lifetime": 120,
            "shootable": False
        }

        if roll == 0:
            target["type"] = "bad_guy"
        elif roll == 1:
            target["type"] = "hostage_shield"
        else:
            target["type"] = "lone_civilian"

        if target["slide_dir"] == "up":
            target["current_x"] = target["target_x"]
            target["current_y"] = target["target_y"] + target["slide_dist"]
        elif target["slide_dir"] == "down":
            target["current_x"] = target["target_x"]
            target["current_y"] = target["target_y"] - target["slide_dist"]
        elif target["slide_dir"] == "left":
            target["current_x"] = target["target_x"] + target["slide_dist"]
            target["current_y"] = target["target_y"]
        elif target["slide_dir"] == "right":
            target["current_x"] = target["target_x"] - target["slide_dist"]
            target["current_y"] = target["target_y"]

        self.active_targets.append(target)
    
    def check_shot(self, mouse_pos):
        pass

    def update(self):
        # Base health engine check
        if self.health <= 0:
            self.health = 0
            self.running = False
            self.success = False

        # Manage spawn intervals
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            self.spawn_target()

        # --- UPDATE ACTIVE TARGET MECHANICS ---
        for target in self.active_targets[:]:
            # 1. State Management & Progress Interpolation
            if target["state"] == "sliding_in":
                target["progress"] += target["slide_speed"]
                if target["progress"] >= 1.0:
                    target["progress"] = 1.0
                    target["state"] = "waiting"
                    target["shootable"] = True  # Fully visible, now vulnerable
                    
            elif target["state"] == "waiting":
                target["lifetime"] -= 1
                if target["lifetime"] <= 0:
                    target["state"] = "sliding_out"
                    target["shootable"] = False  # Moving away, missed window
                    
                    # If a threat times out without being shot, you take damage
                    if target["type"] == "bad_guy" or target["type"] == "hostage_shield":
                        self.health -= self.damage_taken_pct
                        print(f"Ouch! You were shot! Health: {self.health}%")
                    
            elif target["state"] == "sliding_out":
                target["progress"] -= target["slide_speed"]
                if target["progress"] <= 0.0:
                    # Target has hidden completely back behind cover, remove it
                    self.active_targets.remove(target)
                    continue

            # 2. Linear Axis Coordinate Calculation
            inv_p = 1.0 - target["progress"]
            
            if target["slide_dir"] == "up":
                target["current_x"] = target["target_x"]
                target["current_y"] = target["target_y"] + (target["slide_dist"] * inv_p)
            elif target["slide_dir"] == "down":
                target["current_x"] = target["target_x"]
                target["current_y"] = target["target_y"] - (target["slide_dist"] * inv_p)
            elif target["slide_dir"] == "left":
                target["current_x"] = target["target_x"] + (target["slide_dist"] * inv_p)
                target["current_y"] = target["target_y"]
            elif target["slide_dir"] == "right":
                target["current_x"] = target["target_x"] - (target["slide_dist"] * inv_p)
                target["current_y"] = target["target_y"]

    def draw(self):
        self.screen.fill((135, 206, 235))
        
        # 1. RENDER SCENERY LAYER
        for item in self.level_data["scenery"]:
            pygame.draw.rect(self.screen, item["color"], (item["x"], item["y"], item["width"], item["height"]))
            pygame.draw.rect(self.screen, (0, 0, 0), (item["x"], item["y"], item["width"], item["height"]), 2)

        # 2. TARGET CHARACTER POPUP LAYER
        for target in self.active_targets:
            tx, ty, tw, th = target["current_x"], target["current_y"], target["width"], target["height"]
            
            if target["type"] == "bad_guy":
                pygame.draw.rect(self.screen, (255, 140, 0), (tx, ty, tw, th))
            elif target["type"] == "lone_civilian":
                pygame.draw.rect(self.screen, (0, 200, 0), (tx, ty, tw, th))
            elif target["type"] == "hostage_shield":
                pygame.draw.rect(self.screen, (255, 0, 0), (tx, ty, tw, th))
                pygame.draw.rect(self.screen, (0, 200, 0), (tx + 10, ty + 15, tw - 10, th - 15))
                
            pygame.draw.rect(self.screen, (255, 255, 255), (tx, ty, tw, th), 1)

        # 3. RENDER THE HUD / INTERFACE LAYER
        pygame.draw.rect(self.screen, (255, 0, 0), (50, 30, 200, 25))
        health_width = int(200 * (self.health / 100.0))
        pygame.draw.rect(self.screen, (0, 255, 0), (50, 30, health_width, 25))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 30, 200, 25), 2)
        
        for i in range(self.max_ammo):
            color = (255, 215, 0) if i < self.current_ammo else (50, 50, 50)
            pygame.draw.circle(self.screen, color, (300 + (i * 20), 42), 8)
            pygame.draw.circle(self.screen, (0, 0, 0), (300 + (i * 20), 42), 8, 1)

        money_text = self.hud_font.render(f"${int(self.money)}", True, (34, 139, 34))
        self.screen.blit(money_text, (500, 28))
        
        lbl_health = self.font.render("HEALTH", True, (0, 0, 0))
        lbl_ammo = self.font.render("AMMO", True, (0, 0, 0))
        self.screen.blit(lbl_health, (50, 10))
        self.screen.blit(lbl_ammo, (300, 10))

        # 4. INTERACTIVE RETICLE CROSSHAIR
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(self.screen, (255, 0, 0), (mx, my), 15, 2)
        pygame.draw.line(self.screen, (255, 0, 0), (mx - 20, my), (mx + 20, my), 2)
        pygame.draw.line(self.screen, (255, 0, 0), (mx, my - 20), (mx, my + 20), 2)

        pygame.display.flip()

    def run(self):
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