BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]
MAX_SEAT = 72          # seats in a sleeper coach
MAX_DISTANCE_DIGITS = 6


def is_ascii_number(text):
    """Return True if text is a non-empty string of ASCII digits 0-9 only."""
    return isinstance(text, str) and text.isascii() and text.isdigit()


def parse_pnr(pnr):
    """Split a 10 digit PNR into (zone, number). Return None if invalid."""
    if not isinstance(pnr, str):
        return None
    pnr = pnr.strip()
    if len(pnr) != 10 or not is_ascii_number(pnr):
        return None
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """Return total distance from cumulative station distances in CSV form.

    Distances must be non-negative whole numbers in increasing order.
    Return None if the input is invalid.
    """
    if not isinstance(distances_csv, str):
        return None
    parts = [part.strip() for part in distances_csv.split(',')]
    for part in parts:
        if not is_ascii_number(part) or len(part) > MAX_DISTANCE_DIGITS:
            return None
    distances = [int(part) for part in parts]
    pairs = zip(distances, distances[1:])
    if any(later < earlier for earlier, later in pairs):
        return None
    return distances[-1] - distances[0]


def berth_type(seat):
    """Return (coach, berth) for a seat such as "S3-45".

    Return None if the input is invalid.
    """
    if not isinstance(seat, str):
        return None
    parts = seat.strip().split('-')
    if len(parts) != 2:
        return None
    coach, number = parts[0].strip(), parts[1].strip()
    if not coach or not (coach.isascii() and coach.isalnum()):
        return None
    if not is_ascii_number(number) or len(number) > 2:
        return None
    seat_number = int(number)
    if not 1 <= seat_number <= MAX_SEAT:
        return None
    return coach.upper(), BERTHS[seat_number % 8]


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    if result is None:
        print("Invalid PNR: enter exactly 10 digits.")
    else:
        print("Zone and Number:", result)

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    if result is None:
        print("Invalid distances: enter whole numbers in increasing order, "
              "separated by commas.")
    else:
        print("Total Distance:", result)

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    if result is None:
        print("Invalid seat: use COACH-SEAT with a seat "
              f"from 1 to {MAX_SEAT}.")
    else:
        print("Coach and Berth:", result)


if __name__ == "__main__":
    main()
