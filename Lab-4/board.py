class Ship:
    def __init__(self, name, cells):
        self.name = name
        self.cells = frozenset(cells)
        self.hits = set()

    @property
    def sunk(self):
        return self.hits == self.cells


class Board:
    SIZE = 6

    def __init__(self):
        self.ships = set()   # every ship cell (0-indexed (row, col) tuples)
        self.fleet = []      # list of Ship objects
        self.shots = set()

    def place_ship(self, cells, name=None):
        cells = set(cells)
        if not cells:
            raise ValueError("A ship needs at least one cell.")
        for r, c in cells:
            if not (0 <= r < self.SIZE and 0 <= c < self.SIZE):
                raise ValueError(f"Cell {(r, c)} is outside the board.")
        if cells & self.ships:
            raise ValueError("Ships may not overlap.")
        ship = Ship(name or f"Ship {len(self.fleet) + 1}", cells)
        self.fleet.append(ship)
        self.ships.update(cells)
        return ship

    def fire(self, pos):
        """Return (hit, sunk_ship). sunk_ship is the Ship this shot sank, else None."""
        if pos in self.shots:
            raise ValueError("Already fired at that cell.")
        self.shots.add(pos)
        for ship in self.fleet:
            if pos in ship.cells:
                ship.hits.add(pos)
                return True, (ship if ship.sunk else None)
        return False, None

    def ships_remaining(self):
        return sum(1 for s in self.fleet if not s.sunk)

    def all_sunk(self):
        return bool(self.fleet) and all(s.sunk for s in self.fleet) 