# Mathematico

This package represents a game Mathematico as described [here](../README.md).


## Installation

The package is not published yet, therefore in order to install it, you
need to install the package from the github, using the following commands:

> **Warning:**  This code uses folder `./tmp/` as a temporary directory to
download to and extract the package from - this directory gets deleted.

```bash
git clone --quiet https://github.com/balgot/mathematico.git tmp || git -C tmp pull
cd tmp/game && python -m pip install --quiet .
rm -rf tmp
```


## Usage

In order to play the game, you need to supply a `Player` instance to the
`Mathematico` object, e.g.:

```python
from mathematico import Mathematico, RandomPlayer

game = Mathematico()
player1 = RandomPlayer()
game.add_player(player1)
game.add_player(RandomPlayer())
game.play()
```

With the possible output representing achieved score for each player:

```
[90, 70]
```

To see the resulting game board, use:

```python
print(player1.board)
```

```
+--+--+--+--+--+
| 2|13| 3| 8| 7|
+--+--+--+--+--+
|11| 4| 1| 2| 4|
+--+--+--+--+--+
| 3|10| 4| 4| 6|
+--+--+--+--+--+
| 5| 2| 1|12| 3|
+--+--+--+--+--+
|13|12|11|12| 8|
+--+--+--+--+--+
```

### Arena

The class `Mathematico` plays only one game, to simulate multiple rounds,
use the `Arena`:

```python
from mathematico import Arena

arena = Arena()
arena.add_player(player1, verbose=False)
arena.run(rounds=3)
```

which returns the results in each round, e.g.:

```
[[80, 60, 160]]
```



### Players

The package contains implementation of 3 player classes:

* `HumanPlayer` - that uses console input/ouput to interact and accept the
position of the next move
* `RandomPlayer` - this player plays random valid move
* `SimulationPlayer` - this player runs a number of simulations and finds the
move that leads to the largest expected payoff


#### Custom Player

To implement a custom player, it should conform to the interface of abstract
class `Player` and implement the following methods:

* `move(card: int) -> None` - place the card on your board, `self.board` which
is inherited from `Player` base class
    > _note_: this allows for cheating by not placing the numbers immediately, but it is the desired behaviour

* `reset() -> None` - reset the player to the initial state before the next
game can start
