"""
Pokemon TCG Card Definitions
Contains all the card data for the game
"""
from collections import namedtuple
import re
from dataclasses import dataclass
import random
import json

# ─────────────────────────── Data classes ────────────────────────────────────
@dataclass
class Card:
    name: str
    set_code: str
    number: str
    category: str = "Unknown"
    attacks: list = None
    abilities: list = None 
    hp: int = 0
    evolvesTo: str = ""
    evolvesFrom: str = ""
    retreatCost: int = 0
    weaknessto: str = "" 
    damage: int = 0
    action: str = ""
    attacks: dict = None
    description: str = ""
    subtype: str = ""
    attached_energy: list = None

    @property
    def key(self) -> tuple:
        """Unique identifier: (name, set_code, number) – case-insensitive."""
        return (self.name.lower(), self.set_code.upper(), self.number)

    def __str__(self):
        if self.category == "Pokemon":
            return f"{self.name} (Type: {self.category}, Subtype: {self.subtype} , HP: {self.damage}/{self.hp})"
        elif self.category == "Trainer":
            return f"{self.name} (Type: {self.category})"
        elif self.category == "Energy":
            return f"{self.name} (Type: {self.category})"
        

# ─────────────────────────── Deck Creation ───────────────────────────────────
def create_decklist():
    # Get decklist from text file
    try:
        with open("Deck_1.txt", encoding="utf-8") as fh:
            deck_text = fh.read()
    except AttributeError:
        print("[INFO] No deck file given.")
    decklist = parse_deck_string(deck_text)       
            
    random.shuffle(decklist)
    return decklist

# ─────────────────────────── Parsers ─────────────────────────────────────────

# Matches lines like: "3 Snorunt ASC 46"  or  "1 Mega Froslass ex ASC 47"
_LINE_RE = re.compile(
    r"^(?P<qty>\d+)\s+(?P<name>.+?)\s+(?P<set>[A-Z]{2,4})\s+(?P<num>\d+[a-zA-Z]?)$"
)

def parse_deck_string(deck_text: str) -> list[Card]:
    """
    Parse a standard TCG deck list string into DeckCard objects.

    Handles category headers (Pokémon:, Trainer:, Energy:) and
    ignores blank lines, comment lines, and totals.
    """
    cards: list[Card] = []
    current_category = "Unknown"
    card_data = {}  # Initialize card_data as an empty dictionary

    for raw_line in deck_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Section header: "Pokémon: 21", "Trainer: 30", "Energy: 9"
        header_match = re.match(r"^(Pok[eé]mon|Trainer|Energy)\s*:\s*\d*$", line, re.IGNORECASE)
        if header_match:
            label = header_match.group(1).lower()
            if "pok" in label:
                current_category = "Pokemon"
            elif "trainer" in label:
                current_category = "Trainer"
            elif "energy" in label:
                current_category = "Energy"
            continue

        # Check if card is not found in json database
        try:
            with open("card_data.json", "r") as f:
                card_data = json.load(f)
        except FileNotFoundError:
            print("[INFO] card_data.json not found. Creating a new one.")
            card_data = {} 

        m = _LINE_RE.match(line)
        if m:
            #Check if the card is already in the card_data dictionary, if not add it
            if m.group("name").strip() not in card_data:
                add_card(m.group("name").strip(), m.group("set").strip(), m.group("num").strip(), current_category, card_data)
            for x in range(int(m.group("qty"))):
                cards.append(Card(
                    name=m.group("name").strip(),
                    set_code=m.group("set").strip(),
                    number=m.group("num").strip(),
                    category=current_category,
                    hp=card_data.get(m.group("name").strip()).get("hp", 0),
                    subtype=card_data.get(m.group("name").strip()).get("subtype", ""),
                    evolvesTo=card_data.get(m.group("name").strip()).get("evolvesTo", ""),
                    evolvesFrom=card_data.get(m.group("name").strip()).get("evolvesFrom", ""),
                    retreatCost=card_data.get(m.group("name").strip()).get("retreatCost", 0),
                    weaknessto=card_data.get(m.group("name").strip()).get("weaknessto", 0),
                    damage=card_data.get(m.group("name").strip()).get("damage", 0),
                    action=card_data.get(m.group("name").strip()).get("action", ""),
                    description=card_data.get(m.group("name").strip()).get("description", ""),
                    attached_energy=[]
                ))

    return cards

def add_card(name, set_code, number, current_category, card_data):
        card_data[name] = {
                            "name":name,
                            "set_code":set_code,
                            "number":number,
                            "category":current_category,
                            "hp": 0,
                            "subtype": "",
                            "evolvesTo": "",
                            "evolvesFrom": "",
                            "retreatCost": 0,
                            "weaknessto": "",
                            "damage": 0,
                            "action": "",
                            "attacks": {"attack1": {"cost": [], "damage": 0, "Effect": ""},"attack2": {"cost": [], "damage": 0, "Effect": ""}},
                            "description": ""
                        }
        #Save the card data to a json file for future reference
        with open("card_data.json", "w", encoding="utf-8") as f:
            json.dump(card_data, f, ensure_ascii=False, indent=4)

# Test
decklist = create_decklist()
print(f"Decklist contains {len(decklist)} cards:")
for card in decklist:
    print(card)
