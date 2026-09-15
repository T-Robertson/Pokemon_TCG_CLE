# Pokémon TCG Game

A command-line implementation of the Pokémon Trading Card Game. This project simulates the Pokémon TCG in a text-based interface.

**The simulated game is in a testing state**

The core idea was to provide a simplefied game interface for further testing and reporting of the impact of cards and functions
## Features

- Play against a computer opponent with strategic VI *computer opponent needs to be updated
- Energy and Trainer cards * Staduims are also being added, there's just alot of functional interactions to consider
- Prize card system
- Bench Pokémon
- Energy attachment mechanics
- Mulligan handling

## W.I.P

- System Card log
- Card vs card interactions
- Card abilities
- Game Reporting  

## How to Play

1. Run the game:
   ```
   python pokemon_tcg.py
   ```

2. Game Setup:
   - You'll be dealt a hand of 7 cards
   - Choose a basic Pokémon as your active Pokémon
   - Optionally place basic Pokémon on your bench
   - The computer will also set up its side

3. Game Commands:simplified
   - `1-9`: Play the card at that position from your hand
   - `attack`: Attack with your active Pokémon
   - `end`: End your turn
   - `help`: Show available commands
   - `quit`: Quit the game

4. Gameplay Rules:
   - Draw a card at the start of your turn
   - You can play one energy card per turn
   - You can play multiple Pokémon to your bench (up to 5)
   - To attack, your active Pokémon needs enough energy
   - You win by taking all 6 prize cards or defeating all of your opponent's Pokémon

## Game Structure

- **pokemon_tcg.py**: Main game file containing game loop and turn logic
- **player.py**: Player class implementation with deck, hand, and gameplay methods
- **pokemon_cards.py**: Card definitions (Pokémon, Energy, and Trainer cards)
- **game_print.py**: functions that handle the printing to the terminal
- **Deck_#.txt**: Takes in the TCG format for decks, and generates a playable deck
- **card_data.json**: Stores all the card data for card generation

## Requirements

- Python 3.6 or higher

## Project Overview

The game implements a simplified version of the Pokémon Trading Card Game. It follows these core mechanics:

- **Card Types**: Pokémon, Energy, and Trainer cards
- **Evolution**: Basic Pokémon can evolve into more powerful forms
- **Energy System**: Pokémon need energy cards to use attacks
- **Prize Cards**: Take prize cards when you knock out opponent's Pokémon
- **Active and Bench**: One active Pokémon in battle, up to 5 on bench

## Fork Statement
Orginal Repostory: 
https://github.com/Fluid-Technology/TCG

I liked the original idea of ascii art cards, but I am looking to simulate card games, so I need to remove them.

## License

This is a fan project and is not affiliated with or endorsed by Nintendo, The Pokémon Company, or Game Freak.

Enjoy the game! 
