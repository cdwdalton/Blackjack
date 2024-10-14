# Blackjack Game

## Overview

This is a simple command-line Blackjack game implemented in Python. The game allows users to play against a dealer, managing bets and displaying hands. It features multiple functionalities, including hit, stand, and an automatic win condition.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Contributing](#contributing)
- [License](#license)

## Features

- Play against a dealer
- Hit or stand options
- Automatic win for 21
- Betting system with an 'all-in' option
- Customizable player and dealer classes
- Multiple files for better organization

## Installation

To run the Blackjack game locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blackjack-game.git
2. Navigate to the project directory:
   ```bash
   cd blackjack-game
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

1. The goal is to have a hand value closer to 21 than the dealer without going over 21.
2. Players can choose to hit (draw another card) or stand (end their turn).
3. If a player or dealer reaches 21, they win automatically.
4. The game resets hands after each round.


