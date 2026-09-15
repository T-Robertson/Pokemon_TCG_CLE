"""
Player class for Pokémon TCG game
"""
from pokemon_cards import create_decklist

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.is_computer = is_computer
        self.deck = create_decklist()
        self.hand = []
        self.active_pokemon = []
        self.bench = []  # Max 5 Pokémon
        self.discard = []
        self.prizes = []  # Cards set aside as prizes (6 cards)
        self.can_attack = False
        self.is_used_trainer = False
        self.is_attached_energy = False
        self.stadium = None
        self.round = 0
        
    def draw_card(self):
        """Draw a card from the deck to hand"""
        if not self.deck:
            return None  # No cards left, player loses
        
        card = self.deck.pop(0)
        self.hand.append(card)
        return card
    
    def draw_starting_hand(self):
        """Draw the initial 7 cards"""
        for _ in range(7):
            self.draw_card()
    
    def setup_prizes(self):
        """Set up 6 prize cards"""
        for _ in range(6):
            if self.deck:
                self.prizes.append(self.deck.pop(0))
    
    def has_basic_pokemon(self):
        """Check if player has a basic Pokémon in hand"""
        for card in self.hand:
            if card.category == "Pokemon" and card.subtype == "Basic":
                return True
        return False
    
    def mulligan(self):
        """Handle mulligan (no basic Pokémon in starting hand)"""
        # Return cards to deck
        self.deck.extend(self.hand)
        self.hand = []
        # Shuffle deck
        import random
        random.shuffle(self.deck)
        # Draw new hand
        self.draw_starting_hand()
        return not self.has_basic_pokemon()  # Return True if still need to mulligan

    def Shuffle_deck(self,card_index,card):
        import random
        random.shuffle(self.deck)
        self.hand.pop(card_index)
        self.discard.append(card)

    def play_pokemon(self, card_index, as_active=False):
        """Play a Pokémon card from hand"""
        if card_index < 0 or card_index >= len(self.hand):
            return False, "Invalid card index"
        
        card = self.hand[card_index]
        if card.category != "Pokemon":
            return False, "This is not a Pokémon card"
        
        if as_active:
            self.active_pokemon = card
            self.hand.pop(card_index)
            return True, f"Played {card.name} as your active Pokémon"
        elif not card.subtype == "Basic":
            return False, "You can only play Basic Pokémon to the bench"
        elif not as_active and len(self.bench) < 5:
            self.bench.append(card)
            self.hand.pop(card_index)
            return True, f"Played {card.name} to your bench"
        elif not as_active and self.active_pokemon is not None:
            return False, "You already have an active Pokémon"
        else:
            return False, "Your bench is full (max 5 Pokémon)"
    
    def play_energy(self, card_index, target_index=None):
        if not self.is_attached_energy:
            self.is_attached_energy = True
            """Play an energy card from hand onto a Pokémon"""
            if card_index < 0 or card_index >= len(self.hand):
                return False, "Invalid card index"
            
            card = self.hand[card_index]
            if card.category != "Energy":
                return False, "This is not an energy card"
        else:
            return False, "You have already attached an energy this turn"
        
        # Target is active Pokémon
        if target_index is None and self.active_pokemon:
            energy = self.active_pokemon.__getattribute__("attached_energy")
            energy.append(card.name)
            print(energy)
            self.hand.pop(card_index)
            return True, f"Attached {card.name} to {self.active_pokemon.name}"
        # Target is bench Pokémon
        elif target_index is not None and 0 <= target_index < len(self.bench):
            energy = self.bench[target_index].__getattribute__("attached_energy")
            energy.append(card.name)
            print(energy)
            self.hand.pop(card_index)
            return True, f"Attached {card.name} to {self.bench[target_index].name}"
        else:
            return False, "No valid Pokémon target for energy"

# Trainer card effects   
    def play_trainer(self, card_index):
        """Play a trainer card from hand"""
        if card_index < 0 or card_index >= len(self.hand):
            return False, "Invalid card index"
        
        card = self.hand[card_index]
        if card.category != "Trainer":
            return False, "This is not a trainer card"
        
        # Implement effects for different trainer cards
        if card.name == "Potion" and self.active_pokemon:
            self.active_pokemon.hp = min(self.active_pokemon.hp + 20, self.active_pokemon.hp)
            self.hand.pop(card_index)
            self.discard.append(card)
            return True, f"Used Potion to heal {self.active_pokemon.name}"
        
        elif card.name == "Energy Retrieval" and any(c.category == "energy" for c in self.discard):
            energy_cards = [c for c in self.discard if c.category == "energy"]
            if energy_cards:
                energy = energy_cards[0]
                self.discard.remove(energy)
                self.hand.append(energy)
                self.hand.pop(card_index)
                self.discard.append(card)
                return True, "Retrieved an energy card from your discard pile"
        
        elif card.name == "Professor's Research":
            # Discard hand and draw 7 new cards
            discarded_cards = self.hand.copy()
            self.hand = []
            self.discard.extend(discarded_cards)
            for _ in range(7):
                if not self.deck:
                    break
                self.draw_card()
            return True, "Discarded your hand and drew 7 new cards"
        
        elif card.name == "Switch" and self.active_pokemon and self.bench:
            # For simplicity, switch with the first bench Pokémon
            self.active_pokemon, self.bench[0] = self.bench[0], self.active_pokemon
            self.hand.pop(card_index)
            self.discard.append(card)
            return True, f"Switched your active Pokémon with {self.active_pokemon.name}"
        
        elif card.name == "Pokémon Center" and self.active_pokemon:
            # Heal all damage
            self.active_pokemon.hp = self.active_pokemon.hp  # In a real game, would restore to max HP
            self.hand.pop(card_index)
            self.discard.append(card)
            return True, f"Healed all damage from {self.active_pokemon.name}"

        elif card.name == "Lillie's Determination":
            # Shuffle your hand into your deck and draw 6 cards
            self.deck.extend(self.hand)
            self.hand = []
            import random
            random.shuffle(self.deck)
            #If there are greater that 6 prizes, draw 8 cards, otherwise draw 6 cards
            if len(self.prizes) >= 6:
                for _ in range(9):
                    if not self.deck:
                        break
                    self.draw_card()
                self.hand.pop(card_index)
                self.discard.append(card)
                return True, "Shuffled your hand into your deck and drew 8 new cards"
            else:
                for _ in range(7):
                    if not self.deck:
                        break
                    self.draw_card()
                self.hand.pop(card_index)
                self.discard.append(card)
                return True, "Shuffled your hand into your deck and drew 6 new cards"

        elif card.name == "Buddy-Buddy Poffin":
            # Select a 2 Basic Pokemon with less than 70 hp from your deck and put it onto the bench. Then, shuffle your deck.
            basic_pokemon_in_deck = [c for c in self.deck if c.category == "Pokemon" and c.subtype == "Basic" and c.hp <= 70]
            if basic_pokemon_in_deck and len(self.bench) < 5:
                # List basic Pokémon in deck with less than 70 hp
                print("Basic Pokémon in deck with less than 70 HP:")
                for i, pokemon in enumerate(basic_pokemon_in_deck):
                    print(f"{i+1}. {pokemon.name} (HP: {pokemon.hp})")
                # Prompt player to select a Pokémon to put onto the bench
                while True:
                    try:
                        choice = int(input(f"Select a Pokémon to put onto the bench (1-{len(basic_pokemon_in_deck)}): "))
                        if 1 <= choice <= len(basic_pokemon_in_deck):
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(basic_pokemon_in_deck)}.")
                    except ValueError:
                        print("Please enter a valid number.")
                while True:
                    choice2 = int(input(f"Select a second Pokémon to put onto the bench (1-{len(basic_pokemon_in_deck)}): "))
                    try:
                        if 1 <= choice2 <= len(basic_pokemon_in_deck) and choice2 != choice:
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(basic_pokemon_in_deck)} that is not the same as your first choice.")
                    except ValueError:
                        print("Please enter a valid number.")
                new_pokemon1 = basic_pokemon_in_deck[choice - 1]
                new_pokemon2 = basic_pokemon_in_deck[choice2 - 1]
                self.deck.remove(new_pokemon1)
                self.bench.append(new_pokemon1)
                self.deck.remove(new_pokemon2)
                self.bench.append(new_pokemon2)
                #Shuffle Deck and discard Trainer card
                self.Shuffle_deck(card_index,card)
                
                return True, f"Put {new_pokemon1.name} and {new_pokemon2.name} onto your bench and shuffled your deck"

        elif card.name == "Poké Pad":
            #Select Pokemon from the deck that doesnt have a rule box
            Pokemon_in_deck = [c for c in self.deck if c.category == "Pokemon"]
            for i, pokemon in enumerate(Pokemon_in_deck):
                print(f"{i+1}. {pokemon.name} (HP: {pokemon.hp})")
            while True:
                try:
                    choice = int(input(f"Select a Pokémon to put onto the bench (1-{len(Pokemon_in_deck)}): "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
            new_pokemon = Pokemon_in_deck[choice - 1]
            self.deck.remove(new_pokemon)
            self.hand.append(new_pokemon)
            #Shuffle Deck and discard Trainer card
            self.Shuffle_deck(card_index,card)

        elif card.name == "Ultra Ball":
            # Discard two cards and select a Pokemon from your deck and put it onto the bench. Then, shuffle your deck.
            Pokemon_in_deck = [c for c in self.deck if c.category == "Pokemon"]
            if len(self.hand) > 2:
                for x in range(2):
                    while True:
                        try:
                            choice = int(input(f"Select a card to remove for (1-{len(self.hand)}): "))
                            if 1 <= choice <= len(self.hand):
                                break
                            else:
                                print(f"Please enter a number between 1 and {len(self.hand)}.")
                        except ValueError:
                            print("Please enter a valid number.")
                if Pokemon_in_deck and len(self.bench) < 5:
                    print("Pokémon in deck :")
                    for i, pokemon in enumerate(Pokemon_in_deck):
                        print(f"{i+1}. {pokemon.name} (HP: {pokemon.hp})")
                    # Prompt player to select a Pokémon to put onto the bench
                    while True:
                        try:
                            choice = int(input(f"Select a Pokémon to put onto the bench (1-{len(Pokemon_in_deck)}): "))
                            if 1 <= choice <= len(Pokemon_in_deck):
                                break
                            else:
                                print(f"Please enter a number between 1 and {len(Pokemon_in_deck)}.")
                        except ValueError:
                            print("Please enter a valid number.")
                    new_pokemon = Pokemon_in_deck[choice - 1]
                    self.deck.remove(new_pokemon)
                    self.hand.append(new_pokemon)
                    #Shuffle Deck and discard Trainer card
                    self.Shuffle_deck(card_index,card)

        elif card.name == "Risky Ruins":
            self.stadium = "Risk Ruins"
            self.hand.remove(card)
            #add effect for stadium

        return False, "Cannot play this trainer card now"
    
    def attack(self, opponent):
        """Attack the opponent's active Pokémon"""
        if not self.active_pokemon:
            return False, "You don't have an active Pokémon"
        
        if not opponent.active_pokemon:
            return False, "Opponent doesn't have an active Pokémon"
        
        if self.active_pokemon.attached_energy < self.active_pokemon.energy_cost:
            return False, f"Not enough energy to attack (need {self.active_pokemon.energy_cost})"
        
        damage = self.active_pokemon.damage
        opponent.active_pokemon.hp -= damage
        
        result_message = f"{self.active_pokemon.name} used {self.active_pokemon.description} for {damage} damage!"
        
        # Check if the defending Pokémon is knocked out
        if opponent.active_pokemon.hp <= 0:
            opponent.discard.append(opponent.active_pokemon)
            knocked_out_name = opponent.active_pokemon.name
            opponent.active_pokemon = None
            
            # Take a prize card
            if self.prizes:
                prize = self.prizes.pop(0)
                self.hand.append(prize)
                result_message += f"\n{knocked_out_name} was knocked out! You took a prize card."
            
            # Check if all prizes have been taken (win condition)
            if not self.prizes:
                result_message += "\nYou've taken all your prize cards!"
        
        self.can_attack = False  # Can only attack once per turn
        return True, result_message
    
    def choose_new_active(self):
        """Choose a new active Pokémon from the bench"""
        if not self.bench:
            return False, "No Pokémon on bench to promote"
        
        # For simplicity, just promote the first bench Pokémon
        self.active_pokemon = self.bench.pop(0)
        return True, f"Promoted {self.active_pokemon.name} to active"
    
    def start_turn(self):
        """Start a new turn"""
        self.draw_card()
        self.can_attack = True
        
    def make_computer_move(self, opponent):
        """AI logic for computer player's turn"""
        actions = []
        
        # If no active Pokémon, play one
        if not self.active_pokemon:
            for i, card in enumerate(self.hand):
                if card.category == "pokemon":
                    success, message = self.play_pokemon(i, as_active=True)
                    if success:
                        actions.append(message)
                        break
        
        # Play Pokémon to bench
        bench_slots = 5 - len(self.bench)
        pokemon_indices = [i for i, card in enumerate(self.hand) if card.category == "pokemon"]
        for _ in range(min(bench_slots, len(pokemon_indices))):
            idx = pokemon_indices.pop(0)
            success, message = self.play_pokemon(idx, as_active=False)
            if success:
                actions.append(message)
                # Adjust indices for cards that have been removed
                pokemon_indices = [i-1 if i > idx else i for i in pokemon_indices]
        
        # Play one energy card if possible
        energy_indices = [i for i, card in enumerate(self.hand) if card.category == "energy"]
        if energy_indices and self.active_pokemon:
            success, message = self.play_energy(energy_indices[0])
            if success:
                actions.append(message)
        
        # Play useful trainer cards
        trainer_indices = [i for i, card in enumerate(self.hand) if card.category == "trainer"]
        for idx in trainer_indices:
            if len(self.hand) <= idx:  # Skip if card index is now out of range
                continue
            success, message = self.play_trainer(idx)
            if success:
                actions.append(message)
                # Don't play more than one trainer per turn for simplicity
                break
        
        # Attack if possible
        if self.active_pokemon and opponent.active_pokemon and self.can_attack:
            for attacks in self.active_pokemon.attacks:
                if self.active_pokemon.attached_energy == self.attacks :
                    success, message = self.attack(opponent)
                    if success:
                        actions.append(message)
        
        return actions 
