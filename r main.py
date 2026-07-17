def interact_witness(self, params):
        import random
        witness, mode = params # mode is "TALK" or "BRIBE"
        
        if mode == "TALK":
            # Normal investigation: 100% accurate, but drains 2 hours of clock time
            self.session.hours_left -= 2
            self.dialogue_text = f"[{witness['role']}]: {witness['clue_text']}"
        
        elif mode == "BRIBE":
            # Bribery: saves 2 hours of time, but carries a 50% risk of fake intel!
            bribe_amount = witness['bribe_cost']
            if self.session.money_left >= bribe_amount:
                self.session.money_left -= bribe_amount
                
                # 50/50 chance to get lied to because we took the lazy path
                is_lying = random.choice([True, False])
                
                if is_lying:
                    self.dialogue_text = f"[BRIBED] [{witness['role']}]: {witness['fake_clue_text']} (⚠️ Intel feels sketchy...)"
                else:
                    self.dialogue_text = f"[BRIBED] [{witness['role']}]: {witness['clue_text']} (Intel seems secure.)"
            else:
                self.dialogue_text = f"[{witness['role']}]: {witness['failed_text']} (You can't afford the bribe!)"