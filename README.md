
# mip-game

A simple two-player, turn-based number game. The program generates a random sequence of numbers (1–6) and players take turns modifying the sequence to score points.

## Requirements

- Python 3.8 or newer

## Run

- Start the game with:

```bash
python main.py
```

Entry point: main.py

## How To Play

### Setup

- At the start you choose the sequence length (an integer between 15 and 25).
- The program generates a random sequence of that length containing numbers from 1 to 6.
- Two players play alternately. Both players start with 0 points.

### Turn actions

On your turn you must choose one of these actions:

- Sum a pair:
  - Available pairs are fixed by position: (1+2), (3+4), (5+6), … — i.e., first with second, third with fourth, etc.
  - Choose one eligible pair, compute their sum, then replace the two numbers with a single number equal to the sum after applying wrap-around so the result stays in 1–6.
    - If the sum is greater than 6 apply the mapping: 7→1, 8→2, 9→3, 10→4, 11→5, 12→6.
  - You gain 1 point for this action.

- Delete a lone number:
  - If the sequence length is odd there will be an unpaired (lone) number at the end of the sequence.
  - You may delete that lone number on your turn.
  - Deleting a lone number subtracts 1 point from your opponent's score.

### Pairing notes

- Pairing is positional and recalculated after each change. After a pair is replaced by a single number, the sequence reindexes and new pairs are (1+2), (3+4), etc.
- You may only act on one pair (or delete the lone number) per turn.

### End condition and winning

- The game ends when the sequence contains a single number.
- The player with the higher score wins. If scores are equal, the result is a tie.

### Example

- Start sequence: [4, 5, 2, 6, 1] → pairs: (4+5), (2+6) and lone 1.
- If you choose pair (4+5): sum = 9 → wrap to 3, you gain 1 point.
- New sequence becomes [3, 2, 6, 1]. Next player sees pairs (3+2), (6+1).

### Notes

- The wrap rule keeps all numbers in the 1–6 range
- Deleting the lone number is a tactical move that reduces your opponent's score by 1.
