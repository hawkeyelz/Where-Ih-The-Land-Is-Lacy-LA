{
  "case_id": "case_001",
  "title": "The Missing Liberty Bell",
  "difficulty": "Easy",
  "total_hours": 72,
  "total_budget": 1500,
  "rogue": {
    "name": "Vinnie Velocity",
    "hair": "Slicked Black",
    "vehicle": "Convertible",
    "hobby": "Tennis",
    "feature": "Gold Ring"
  },
  "route": ["Philadelphia", "London", "Cairo"],
  "locations": {
    "Philadelphia": {
      "city_name": "Philadelphia",
      "country": "USA",
      "image_key": "philadelphia_bg",
      "description": "The historic streets of Philly feel unusually quiet. Someone saw a slick-haired thief speeding away from Independence Hall.",
      "witnesses": [
        {
          "role": "Bank Teller",
          "personality": "greedy",
          "bribe_cost": 100,
          "is_locked": false,
          "is_hostage": false,
          "clue_text": "He was converting his cash to British Pounds. Kept boasting about outrunning Big Ben.",
          "failed_text": "I don't talk to broke detectives. Bring cash.",
          "fake_clue_text": "Oh yeah, he changed all his money to Euros. Said something about wanting to see the Eiffel Tower in Paris."
        },
        {
          "role": "Hotel Concierge",
          "personality": "friendly",
          "bribe_cost": 0,
          "is_locked": true,
          "is_hostage": false,
          "clue_text": "He asked for a map of the River Thames and mentioned he was in town for a tennis match.",
          "failed_text": "Pardon me, but I only discuss hotel guests with polite, charming individuals.",
          "fake_clue_text": "He asked for travel brochures for Tokyo. He seemed very excited about sushi."
        }
      ]
    },
    "London": {
      "city_name": "London",
      "country": "United Kingdom",
      "image_key": "london_bg",
      "description": "Fog rolls over the Thames. The local constabulary confirms a mysterious traveler matching Vinnie's slick look arrived on a flight.",
      "witnesses": [
        {
          "role": "Museum Curator",
          "personality": "stubborn",
          "bribe_cost": 0,
          "is_locked": false,
          "is_hostage": true,
          "clue_text": "He was asking about ancient Egyptian hieroglyphics. Said he was heading to Cairo next.",
          "failed_text": "You don't intimidate me. Get out of my museum!",
          "fake_clue_text": "He was muttering about the Sydney Opera house. Bound for Australia, I wager."
        },
        {
          "role": "Cab Driver",
          "personality": "greedy",
          "bribe_cost": 50,
          "is_locked": false,
          "is_hostage": false,
          "clue_text": "I dropped him off near a flight heading to the Nile. I noticed a massive gold ring on his pinky finger.",
          "failed_text": "Gas ain't free, pal. No money, no talk.",
          "fake_clue_text": "Dropped him off at the terminal for flights to Rio. Said he wanted to dance the Samba."
        }
      ]
    },
    "Cairo": {
      "city_name": "Cairo",
      "country": "Egypt",
      "image_key": "cairo_bg",
      "description": "The heat rises off the desert sands. You track the footprints right to the base of the Great Pyramid...",
      "witnesses": [
        {
          "role": "Souk Vendor",
          "personality": "friendly",
          "bribe_cost": 0,
          "is_locked": false,
          "is_hostage": false,
          "clue_text": "I saw him! He was carrying a massive bronze bell wrapped in a blanket. Go get him, Lacy!",
          "failed_text": "I don't know who you are. Go away!",
          "fake_clue_text": "Never heard of him. Try looking in Antarctica."
        }
      ]
    }
  }
}