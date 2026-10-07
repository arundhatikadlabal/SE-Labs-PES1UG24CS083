from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Internal coordinates are 0-indexed (row, col) tuples.
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Ship cells remaining:", len(self.enemy.ships - self.enemy.shots))

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)  # 1-indexed input -> 0-indexed internal
            except ValueError:
                print("Use row,col.")
                continue
            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue
            print("HIT!" if self.enemy.fire(pos) else "MISS!")
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()  # 0-indexed (row, col) tuple
            # 0-indexed internal -> 1-indexed for display
            print(f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}")
            if self.player.fire(ai_pos):
                print("AI scored a hit.")
            if self.player.all_sunk():
                print("The AI sank your fleet.")
                return 