import sqlite3

class ActiveSession:
    def __init__(self, case_id):
        self.case_id = case_id
        
        # Load starting caps directly from the case dossier definitions
        conn = sqlite3.connect("lacy_la.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, total_hours, total_budget FROM cases WHERE case_id = ?", (case_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            self.title = row[0]
            self.hours_left = row[1]
            self.money_left = row[2]
        else:
            self.title = "Unknown Case"
            self.hours_left = 72
            self.money_left = 1500

        # Lacy's Kinetic Inventory Status
        self.current_city = "Philadelphia"  # Matches our step-1 start route position
        self.bullets_chambered = 6
        self.bullets_reserve = 6           # Max hard cap: 12 total rounds
        self.vehicle_type = "none"         # options: 'none' (Bus), 'basic_car', 'fast_car'
        self.has_lockpick_kit = False

    def process_travel(self, travel_type):
        """
        Handles resource changes for long-distance city hops.
        """
        if travel_type == "private_charter":
            self.money_left -= 800
            self.hours_left -= 3
        elif travel_type == "commercial":
            self.money_left -= 300
            self.hours_left -= 14

    def process_local_transport(self, transport_choice):
        """
        Handles upgrading vehicle tiers inside a city.
        """
        if transport_choice == "fast_car" and self.money_left >= 400:
            self.money_left -= 400
            self.vehicle_type = "fast_car"
            return True
        elif transport_choice == "basic_car" and self.money_left >= 150:
            self.money_left -= 150
            self.vehicle_type = "basic_car"
            return True
        elif transport_choice == "bus":
            self.vehicle_type = "none"
            return True
        return False

    def apply_civilian_penalty(self):
        """Slaps Lacy with financial medical liabilities if she hits an innocent."""
        self.money_left -= 500  # Stiff penalty for sloppy shooting
        print(f"Liability Penalty Applied! Money Remaining: ${self.money_left}")