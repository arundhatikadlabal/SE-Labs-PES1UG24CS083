import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.targets = []  # untried cells adjacent to a hit (0-indexed)

    def choose(self):
        """Return a 0-indexed (row, col) tuple, or None if no cells remain."""
        # Drop any target that has been tried since it was queued
        self.targets = [p for p in self.targets if p not in self.tried]
        if self.targets:
            pos = random.choice(self.targets)
            self.targets.remove(pos)
        else:
            options = [(r, c) for r in range(self.size) for c in range(self.size)
                       if (r, c) not in self.tried]
            if not options:
                return None
            pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def report(self, pos, hit):
        """Tell the AI the result of its shot; on a hit, queue the 4 neighbours."""
        if not hit:
            return
        r, c = pos
        for n in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if (0 <= n[0] < self.size and 0 <= n[1] < self.size
                    and n not in self.tried and n not in self.targets):
                self.targets.append(n) 