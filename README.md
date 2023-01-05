# Mathematico

A classic game, for unlimited number of players. Each player keeps track of
their own board and after 25 random choices of numbers, the score is calculated
for each player and the highest score wins.

> **note**: You can try it!
    <ul>
        <li>[on Google Colab](https://colab.research.google.com/drive/1HuVb5_FK9T3tkA8OjjQ40LhsSiQ1wlXm?usp=sharing) this is the version that uses rules as descibed in this README
        </li>
        <li>[other implementation](https://yetty.github.io/Matematico/) with the description in Czech language
        </li>
    </ul>


## Rules of the Game

The game of Mathematico is played on a *5x5 grid*. In each round, a card with a number is drawn
from the deck consisting of cards with numbers in range 1-13, with 4 copies of each, and players
are obliged to fill the number in one of the empty cells on their board. When the boards are full,
resulting scores are computed (see below) for each board, and the player with the highest score wins.

### Scoring System

For each line, row and two longest diagonals, the points are computed based on the following table
and are summed across all rows, columns and diagonals. In addition, if the score in a diagonal
is non-zero, the player is awarded *10 bonus points* for each such diagonal.

*The numbers in the rows, columns and diagonals can be in __ANY__ order.*


|             Rule                 |     Example    | Points
|--------------------------------- | -------------- | -------
|    One pair                      |  1  2  3  4  1 |   10
|    Two pairs                     |  1  2  2  3  1 |   20
|    Three of a kind               |  5  6  7  7  7 |   40
|    Full House                    |  1  1  2  2  2 |   80
|    Four of a kind (not number 1) |  1  2  2  2  2 |  160
|    Four ones                     |  1  1  5  1  1 |  200
|    Straight                      |  5  7  9  8  6 |   50
|    Three 1s and two 13s          |  1 13  1 13  1 |  100
|    Numbers 1, 10, 11, 12, 13     | 12 11 13  1 10 |  150


For each row, column and diagonal, only the highest score is applied, i.e. it is forbidden
to combine two scoring rules for one line.
