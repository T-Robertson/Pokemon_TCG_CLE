"""
Print Functions for Pokémon TCG Game
"""

def print_title():
    """Print the game title in ASCII art"""
    print("""
 _____      _                              _______ _____ _____  
|  __ \\    | |                            |__   __/ ____|  __ \\ 
| |__) |__ | | _____ _ __ ___   ___  _ __    | | | |    | |  | |
|  ___/ _ \\| |/ / _ \\ '_ ` _ \\ / _ \\| '_ \\   | | | |    | |__| |
| |  | (_) |   <  __/ | | | | | (_) | | | |  | | | |____| |_| | 
|_|   \\___/|_|\\_\\___|_| |_| |_|\\___/|_| |_|  |_|  \\_____|____/ 
                                                               
    """)

def print_hand(hand):
    """Print the player's hand in a more detailed way"""
    print("\nYOUR HAND:")
    print("=" * 80)
    
    for i, card in enumerate(hand):
        print(f"{i+1}. {card}")
        print("-" * 40)
    
    print("=" * 80)

def print_board(player, computer, show_computer_hand=False):
    """Print the current game board"""
    print("\n" + "=" * 80)
    print("COMPUTER".center(80))
    print(f"Deck: {len(computer.deck)} cards | Discard: {len(computer.discard)} cards")
    
    print("\nCOMPUTER'S ACTIVE POKEMON:")
    if computer.active_pokemon:
        print(computer.active_pokemon)
    else:
        print("No active Pokémon")

    
    print("\nCOMPUTER'S BENCH:")
    if computer.bench:
            for pokemon in computer.bench:
                print(f"{pokemon.name} {pokemon.damage}/{pokemon.hp}")
    else:
        print("No Pokémon on bench")
    
    if show_computer_hand:
        print("\nCOMPUTER'S HAND:")
        for card in computer.hand:
            print(f"- {card}")
    else:
        print(f"\nCOMPUTER'S HAND: {len(computer.hand)} cards")
    
    print("\n" + "-" * 80 + "\n")
    print(f"| Stadium: {player.stadium} | Round {None}") #Add round counter
    print("\n" + "-" * 80 + "\n")
    
    print("PLAYER".center(80))
    print(f"Deck: {len(player.deck)} cards | Discard: {len(player.discard)} cards")
    
    print("\nYOUR ACTIVE POKEMON:")
    if player.active_pokemon:
        if len(player.active_pokemon.attached_energy) > 0:
            print(f"{player.active_pokemon} {player.active_pokemon.attached_energy}")
        else:
            print(f"{player.active_pokemon}")
    else:
        print("No active Pokémon")
    
    print("\nYOUR BENCH:")
    if player.bench:
        for pokemon in player.bench:
            if len(pokemon.attached_energy) > 0:
                print(f"{pokemon.name} {pokemon.damage}/{pokemon.hp} {pokemon.attached_energy}")
            print(f"{pokemon.name} {pokemon.damage}/{pokemon.hp}")
    else:
        print("No Pokémon on bench")
    
    print("\nYOUR HAND:")
    for i, card in enumerate(player.hand):
        print(f"{i+1}. {card}")
    
    print("=" * 80 + "\n")

def print_turn_banner(player_name):
    """Print a banner for whose turn it is"""
    banner = f"===== {player_name}'S TURN ====="
    print("\n" + "=" * len(banner))
    print(banner)
    print("=" * len(banner) + "\n")

def print_action(action_text):
    """Print an action with formatting"""
    print(f">> {action_text}")

def print_winner(winner):
    """Print the winner announcement"""
    print("\n" + "*" * 60)
    print(f"***** {winner} WINS THE GAME! *****".center(60))
    print("*" * 60 + "\n")

def print_help():
    """Print help information"""
    print("\n=== COMMANDS ===")
    print("1-N       - Play card from hand (number corresponds to card position)")
    print("attack    - Attack with your active Pokémon")
    print("end       - End your turn")
    print("help      - Show this help information")
    print("quit      - Quit the game")
    print("==============\n") 