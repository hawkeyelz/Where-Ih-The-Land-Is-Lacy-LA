import sys
import random
import pygame
import db_manager
from lockpick_game import LockpickMinigame

class GameSession:
    def __init__(self):
        self.case_id = "case_001"
        self.case_meta = db_manager.load_case(self.case_id)
        self.current_city = "Philadelphia"
        self.money_left = self.case_meta["total_budget"] if self.case_meta else 1500
        self.hours_left = self.case_meta["total_hours"] if self.case_meta else 72
        self.is_game_over = False
        self.victory = False

class LacyLaGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Lacy La: Private Eye")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.bold_font = pygame.font.SysFont("Arial", 22, bold=True)
        self.header_font = pygame.font.SysFont("Arial", 32, bold=True)
        
        self.session = GameSession()
        self.current_location_data = None
        self.witnesses = []
        self.dialogue_text = "Select a witness or action to investigate the scene."
        self.buttons = []
        
        self.load_current_scene()

    def load_current_scene(self):
        """Loads data from our database module for the active city."""
        self.current_location_data = db_manager.load_location(
            self.session.case_id, self.session.current_city
        )
        self.witnesses = db_manager.load_witnesses_for_location(
            self.session.case_id, self.session.current_city
        )
        self.dialogue_text = f"Arrived in {self.session.current_city}. What's our plan, Lacy?"
        self.rebuild_ui()

    def rebuild_ui(self):
        """Recreates interactive buttons based on active witnesses and actions."""
        self.buttons = []
        
        # We start witness buttons Y positioning lower down on the screen
        y_offset = 320
        for idx, witness in enumerate(self.witnesses):
            # Create a bounding box for the witness action panel
            witness_panel_rect = pygame.Rect(50, y_offset, 700, 70)
            
            # Action button setup based on lock/bribe properties
            action_btn_rect = pygame.Rect(580, y_offset + 15, 150, 40)
            
            if witness["is_locked"]:
                label = "LOCKPICK"
                action_type = "MINIGAME"
            else:
                label = f"BRIBE (${witness['bribe_cost']})" if witness['bribe_cost'] > 0 else "TALK"
                action_type = "BRIBE" if witness['bribe_cost'] > 0 else "TALK"
            
            self.buttons.append({
                "rect": action_btn_rect,
                "label": label,
                "type": action_type,
                "witness_data": witness,
                "panel_rect": witness_panel_rect
            })
            y_offset += 85

        # Add a transition button to fly to the next logical location
        # Philadelphia leads to London, London to Cairo, Cairo is the finish.
        next_destination = None
        if self.session.current_city == "Philadelphia":
            next_destination = "London"
        elif self.session.current_city == "London":
            next_destination = "Cairo"

        if next_destination:
            self.buttons.append({
                "rect": pygame.Rect(580, 500, 150, 40),
                "label": f"FLY TO {next_destination.upper()}",
                "type": "TRAVEL",
                "destination": next_destination,
                "panel_rect": None
            })

    def handle_click(self, pos):
        """Processes clicking events for witness options and minigames."""
        if self.session.is_game_over:
            return

        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                if btn["type"] == "TRAVEL":
                    self.session.current_city = btn["destination"]
                    self.session.hours_left -= 6  # Travel costs time!
                    self.load_current_scene()
                    
                elif btn["type"] == "TALK":
                    # Clean, normal conversation
                    self.session.hours_left -= 2
                    self.dialogue_text = f"[{btn['witness_data']['witness_role']}]: {btn['witness_data']['clue_text']}"
                    
                elif btn["type"] == "BRIBE":
                    # 50% probability of receiving the Fake Clue database entry
                    bribe = btn["witness_data"]["bribe_cost"]
                    if self.session.money_left >= bribe:
                        self.session.money_left -= bribe
                        is_lying = random.choice([True, False])
                        
                        if is_lying:
                            self.dialogue_text = f"[BRIBED] [{btn['witness_data']['witness_role']}]: {btn['witness_data']['fake_clue_text']} (⚠️ Intel feels sketchy...)"
                        else:
                            self.dialogue_text = f"[BRIBED] [{btn['witness_data']['witness_role']}]: {btn['witness_data']['clue_text']} (Intel seems secure.)"
                    else:
                        self.dialogue_text = f"[{btn['witness_data']['witness_role']}]: {btn['witness_data']['failed_text']} (No cash!)"
                        
                elif btn["type"] == "MINIGAME":
                    # Launch the modular lockpicking screen
                    lock_game = LockpickMinigame(self.screen)
                    success = lock_game.run()
                    
                    # Return to main screen configuration
                    pygame.display.set_caption("Lacy La: Private Eye")
                    
                    if success:
                        # Unlock the witness permanently in this runtime session
                        btn["witness_data"]["is_locked"] = False
                        self.dialogue_text = f"[SUCCESS] You picked the lock! [{btn['witness_data']['witness_role']}]: {btn['witness_data']['clue_text']}"
                    else:
                        self.session.hours_left -= 4 # Penalize time for failing/quitting
                        self.dialogue_text = "[FAILED] The tumbler snapped. You wasted hours struggling with the locked door."
                    
                    self.rebuild_ui()

    def update(self):
        # Quick Win/Loss condition checks
        if self.session.hours_left <= 0:
            self.session.is_game_over = True
            self.session.victory = False
        elif self.session.current_city == "Cairo" and "bronze bell" in self.dialogue_text.lower():
            self.session.is_game_over = True
            self.session.victory = True

    def draw(self):
        self.screen.fill((30, 32, 40)) # Dark midnight blue slate
        
        # Render Top HUD Panel
        hud_bg = pygame.Rect(0, 0, 800, 80)
        pygame.draw.rect(self.screen, (24, 26, 32), hud_bg)
        
        title_lbl = self.header_font.render("LACY LA: DETECTIVE", True, (97, 175, 239))
        time_lbl = self.font.render(f"CLOCK: {self.session.hours_left} Hrs Left", True, (224, 108, 117))
        cash_lbl = self.font.render(f"BUDGET: ${self.session.money_left}", True, (152, 195, 121))
        
        self.screen.blit(title_lbl, (20, 20))
        self.screen.blit(time_lbl, (480, 30))
        self.screen.blit(cash_lbl, (650, 30))
        
        # Render Active Scene Information
        if self.current_location_data:
            loc_title = self.bold_font.render(
                f"CURRENT LOCATION: {self.current_location_data['city_name']}, {self.current_location_data['country']}", 
                True, (229, 192, 123)
            )
            self.screen.blit(loc_title, (50, 100))
            
            # Simple word-wrapping description card rendering
            desc_y = 135
            desc_words = self.current_location_data['description'].split(' ')
            line = ""
            for word in desc_words:
                test_line = line + " " + word if line else word
                if self.font.size(test_line)[0] < 700:
                    line = test_line
                else:
                    self.screen.blit(self.font.render(line, True, (171, 178, 191)), (50, desc_y))
                    desc_y += 22
                    line = word
            self.screen.blit(self.font.render(line, True, (171, 178, 191)), (50, desc_y))

        # Render Core Dialogue Box
        dialogue_panel = pygame.Rect(50, 210, 700, 90)
        pygame.draw.rect(self.screen, (40, 44, 52), dialogue_panel)
        pygame.draw.rect(self.screen, (97, 175, 239), dialogue_panel, 2)
        
        # Render wrapped text for witness dialogue output
        dia_y = 220
        dia_words = self.dialogue_text.split(' ')
        line = ""
        for word in dia_words:
            test_line = line + " " + word if line else word
            if self.font.size(test_line)[0] < 660:
                line = test_line
            else:
                self.screen.blit(self.font.render(line, True, (255, 255, 255)), (70, dia_y))
                dia_y += 22
                line = word
        self.screen.blit(self.font.render(line, True, (255, 255, 255)), (70, dia_y))

        # Render interactive elements & action choices
        for btn in self.buttons:
            if btn["panel_rect"]:
                # Draw witness base plate panel
                pygame.draw.rect(self.screen, (40, 44, 52), btn["panel_rect"])
                pygame.draw.rect(self.screen, (75, 82, 99), btn["panel_rect"], 1)
                
                # Witness detail tag inside panel
                role = btn["witness_data"]["witness_role"]
                pers = btn["witness_data"]["personality"].upper()
                lock_status = " [LOCKED]" if btn["witness_data"]["is_locked"] else ""
                witness_lbl = self.bold_font.render(f"{role} ({pers}){lock_status}", True, (229, 192, 123))
                self.screen.blit(witness_lbl, (70, btn["panel_rect"].y + 22))
            
            # Draw Button Trigger Core
            btn_color = (97, 175, 239) if btn["type"] != "TRAVEL" else (152, 195, 121)
            pygame.draw.rect(self.screen, btn_color, btn["rect"])
            
            lbl_surf = self.font.render(btn["label"], True, (24, 26, 32))
            lbl_rect = lbl_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(lbl_surf, lbl_rect)

        # Render Endscreens on GameOver state
        if self.session.is_game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(220)
            overlay.fill((20, 20, 20))
            self.screen.blit(overlay, (0,0))
            
            if self.session.victory:
                end_msg = "CASE SOLVED! Lacy recovered the Liberty Bell!"
                color = (152, 195, 121)
            else:
                end_msg = "CASE COLD: Lacy ran out of time!"
                color = (224, 108, 117)
                
            msg_surf = self.header_font.render(end_msg, True, color)
            msg_rect = msg_surf.get_rect(center=(400, 280))
            self.screen.blit(msg_surf, msg_rect)
            
            restart_lbl = self.font.render("Press Escape to exit and restart.", True, (171, 178, 191))
            restart_rect = restart_lbl.get_rect(center=(400, 350))
            self.screen.blit(restart_lbl, restart_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            self.update()
            self.draw()

if __name__ == "__main__":
    game = LacyLaGame()
    game.run()