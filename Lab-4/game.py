from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Ship cells remaining:", len(self.enemy.ships - self.player.shots))

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue
            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue
            if pos in self.player.shots:
                print("Already fired there.")
                continue
            print("HIT!" if self.enemy.fire(pos) else "MISS!")
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()

            # representation consistent through the whole flow.
            try:
                ar, ac = map(int, ai_pos.split(","))
                player_pos = (ar, ac)
            except ValueError:
                player_pos = None
            if player_pos is not None:
                print("AI fired at", ai_pos)
                if player_pos in self.player.ships:
                    print("AI scored a hit.")
