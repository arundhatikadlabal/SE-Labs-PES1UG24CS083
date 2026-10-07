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
        # Fleet: sizes 3, 2, 2, no overlaps (Board.place_ship enforces this).
        self.player.place_ship({(1, 1), (1, 2), (1, 3)}, "Cruiser")
        self.player.place_ship({(3, 0), (4, 0)}, "Destroyer")
        self.player.place_ship({(5, 3), (5, 4)}, "Submarine")

        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)}, "Cruiser")
        self.enemy.place_ship({(0, 5), (1, 5)}, "Destroyer")
        self.enemy.place_ship({(4, 0), (4, 1)}, "Submarine")

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Ship cells remaining:", len(self.enemy.ships - self.enemy.shots))
        print("Enemy ships remaining:", self.enemy.ships_remaining())

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
                print(f"You already fired at {pos[0] + 1},{pos[1] + 1}. Choose another cell.")
                continue

            hit, sunk = self.enemy.fire(pos)
            print("HIT!" if hit else "MISS!")
            if sunk:
                print(f"You sank the enemy {sunk.name}!")
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()  # 0-indexed (row, col) tuple, or None
            if ai_pos is None:
                print("AI has no cells left to fire at.")
                continue
            # 0-indexed internal -> 1-indexed for display
            print(f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}")
            hit, sunk = self.player.fire(ai_pos)
            self.ai.report(ai_pos, hit)
            if hit:
                print("AI scored a hit.")
            else:
                print("AI missed.")
            if sunk:
                print(f"The AI sank your {sunk.name}!")
            if self.player.all_sunk():
                print("The AI sank your fleet.")
                return 