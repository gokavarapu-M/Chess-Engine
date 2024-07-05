# Python Chess Engine

A fully-functional chess engine developed in Python, featuring both human vs. human and human vs. AI gameplay modes. The project utilizes Pygame for the graphical user interface and implements advanced AI algorithms for computer opponents.

## Features

- Complete implementation of chess rules
- Graphical user interface using Pygame
- Two game modes: Human vs. Human and Human vs. AI
- AI opponent powered by Minimax and Negamax algorithms with Alpha-Beta Pruning
- Undo function to revert moves
- Live move log to track the game

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository:
   ```bash
   git clone https://github.com/gokavarapu-M/Chess-Engine.git
   ```
3.Navigate to project directory:
```bash
cd Chess-Engine/Chess
```
4. Install the required dependencies
   ```bash
   pip install pugame
   ```

## Usage
Run the main script to start the chess game:
```bash
python ChessMain.py
```

## Game Mode Configuration
To play Human vs. Human or Human vs. AI, adjust the game mode variable inside the code:

1. Open ChessMain.py in a text editor.
2. [Go to line 50](https://github.com/gokavarapu-M/Chess-Engine/blob/main/Chess/ChessMain.py#L50)
 for game mode settings.
3. Set the appropriate variable for the desired game mode:
```python
playerOne = True # white is Human
playerTwo = False # black is AI

#or
playerOne = False # white is AI
playerTwo = True # black is human

#or

playerOne = True # white is Human
playerTwo = True #black is Human
```

## AI Algorithm

The AI opponent uses the Minimax algorithm with Alpha-Beta Pruning for efficient move evaluation. The Negamax variation is also implemented for optimized performance.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the  [issues page](https://github.com/gokavarapu-M/Chess-Engine/issues) if you want to contribute.





