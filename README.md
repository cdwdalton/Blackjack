# Blackjack Game

## Overview

This is a simple command-line Blackjack game implemented in Python. The game allows users to play against a dealer, managing bets and displaying hands. It features multiple functionalities, including hit, stand, and an automatic win condition.

## Features

- Play against a dealer
- Hit or stand options
- Automatic win for 21
- Betting system with an 'all-in' option
- Customizable player and dealer classes
- Multiple files for better organization
- If you have no more chips left, the game will stop and ask you if you want to play another hand, you can reply 'y' or 'n'.

## Prerequisites

To run this game, you need to have Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

## Installation

To run the Blackjack game locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/cdwdalton/Blackjack.git
2. Navigate to the project directory:
   ```bash
   cd Blackjack
3. (Optional) Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
4. Install any necessary dependancies:
   ```bash
   pip install -r requirements.txt

## Usage

To start the game, run the following command in your terminal:
```bash
python blackjack.py
```
Follow the on-screen instructions to place your bets and play against the dealer.

## Controls

* To **Hit** (draw another card), press '**h**'.
* To **Stand** (end your turn), press '**s**'.
* To bet **All in**, type '**all**'

## Game Rules

1. The goal of the game is to have a hand value as close to 21 as possible without exceeding it.
2. Aces can be valued at either 1 or 11.
3. Face cards (Kings, Queens, and Jacks) are valued at 10.
4. Players can choose to hit (take another card) or stand (keep their current hand).
5. If the player's hand exceeds 21, they bust and lose the game.
6. If the player and dealer have the same hand value, it's a push.

## Code Structure

* blackjack.py: Main game logic and execution.
* card.py: Class defining card properties and behaviors.
* deck.py: Class for managing the deck of cards.
* player.py: Class representing the player and dealer, including their hands and betting system.
* constants.py: Constants used throughout the game for settings and configurations.
