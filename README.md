twisted-pentago
=================

This project is a server to which clients can connect via TCP to play a game of Pentago.

## Instructions
Run `python pentagoM.py` in one terminal window.   
Run `python client.py` in two separate terminal windows.

To play in just one terminal window, run `python pentagoS.py` (this does not require twisted).

## Requirements
*   [Python 2.x](https://www.python.org/)
*   [Twisted](https://twistedmatrix.com/)

## Gameplay
Possible moves are lettered `A` to `D` and numbered `1` through `9`, left-to-right, top-to-bottom (top-left is A, bottom-right is D and top-left is 1, bottom-right is 9).

    A1 A2 A3 | B1 B2 B3
    A4 A5 A6 | B4 B5 B6
    A7 A8 A9 | B7 B8 B9
    ---------+---------
    C1 C2 C3 | D1 D2 D3
    C4 C5 C6 | D4 D5 D6
    C7 C8 C9 | D7 D8 D9

Possible moves are lettered `A` to `D`, with either a `'` or `"`, being to rotate clockwise or counterclockwise, respectively.

             |
        A    |    B 
             |
    ---------+---------
             |
        C    |    D
             |
             
## Rules
The rules for Pentago can be found [here](http://www.mindtwisterusa.com/pdfs/Strategy_Guide.pdf).
             
