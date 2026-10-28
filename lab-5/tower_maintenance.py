"""Maintenance tracker for telecom towers: logs towers, servicing and risk."""
import sqlite3


class TowerTracker:
    """Keeps tower records in an in-memory SQLite database."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE towers (id INTEGER PRIMARY KEY, site TEXT, "
            "last_service INTEGER, faults INTEGER)"
        )
        self.service_count = 0

    def add_tower(self, site, last_service, faults=0):
        """Add a tower with its last service year and current fault count."""
        self.conn.execute(
            "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
            (site, last_service, faults),
        )
        self.conn.commit()

    def service_tower(self, tower_id, year):
        """Record that a tower was serviced in the given year.

        Servicing also clears the tower's fault count.
        """
        try:
            self.conn.execute(
                "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
                (year, tower_id),
            )
            self.service_count += 1
        except sqlite3.Error:
            print("service failed")

    def overdue(self, year):
        """Return the sites not serviced in the two years before `year`."""
        rows = self.conn.execute(
            "SELECT site, last_service FROM towers"
        ).fetchall()
        result = []
        for site, last in rows:
            if year - last >= 2:
                result.append(site)
        return result

    def risk_level(self, tower_id):
        """Rate a tower as high risk if it has more than three faults."""
        row = self.conn.execute(
            "SELECT faults FROM towers WHERE id = ?", (tower_id,)
        ).fetchone()
        if row is None:
            return "unknown"
        if row[0] > 3:
            return "high"
        return "normal"

    def snapshot(self):
        """Return a copy of every tower record."""
        return list(self.conn.execute("SELECT * FROM towers").fetchall())


def main():
    """Run a short demonstration of the tracker."""
    tracker = TowerTracker()
    tracker.add_tower("Ridge-A", 2021, 5)
    tracker.add_tower("Coast-B", 2024)
    tracker.service_tower(2, 2025)
    total = len(tracker.snapshot())
    print(
        tracker.overdue(2025),
        tracker.risk_level(1),
        total,
        tracker.service_count,
    )


if __name__ == "__main__":
    main()
