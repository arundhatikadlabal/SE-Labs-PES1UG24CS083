from hypothesis import given, strategies as st
from train_fare import parse_pnr, journey_distance, berth_type, BERTHS


# ---------- parse_pnr ----------

@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):
    try:
        parse_pnr(s)
    except Exception as e:
        assert False, f"parse_pnr crashed with: {e!r}"


@given(st.from_regex(r"\A[0-9]{10}\Z"))
def test_parse_pnr_valid(pnr):
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))


@given(st.text(alphabet="0123456789").filter(lambda s: len(s) != 10))
def test_parse_pnr_rejects_wrong_length(pnr):
    # a PNR must be exactly 10 digits
    assert parse_pnr(pnr) is None


# ---------- journey_distance ----------

@given(st.text() | st.none())
def test_journey_distance_no_crash(s):
    try:
        journey_distance(s)
    except Exception as e:
        assert False, f"journey_distance crashed with: {e!r}"


@given(st.lists(st.text(alphabet="0123456789- "), max_size=5).map(",".join))
def test_journey_distance_malformed_csv_no_crash(s):
    # CSV-like strings with empty, negative and padded values
    try:
        journey_distance(s)
    except Exception as e:
        assert False, f"journey_distance crashed with: {e!r}"


DISTANCE = st.integers(min_value=0, max_value=5000)


@given(st.lists(DISTANCE, min_size=1, max_size=10))
def test_journey_distance_valid(distances):
    distances.sort()
    csv = ",".join(str(d) for d in distances)
    result = journey_distance(csv)
    assert result == distances[-1] - distances[0]
    assert result >= 0


@given(st.lists(DISTANCE, min_size=2, max_size=10))
def test_journey_distance_never_negative(distances):
    # distances in any order: the result is either rejected or non-negative
    result = journey_distance(",".join(str(d) for d in distances))
    assert result is None or result >= 0


# ---------- berth_type ----------

@given(st.text() | st.none())
def test_berth_type_no_crash(s):
    try:
        berth_type(s)
    except Exception as e:
        assert False, f"berth_type crashed with: {e!r}"


@given(st.from_regex(r"\A[A-Za-z][0-9]{0,2}\Z"),
       st.integers(min_value=1, max_value=72))
def test_berth_type_valid(coach, seat):
    assert berth_type(f"{coach}-{seat}") == (coach.upper(), BERTHS[seat % 8])


@given(st.from_regex(r"\A[A-Za-z0-9]{0,3}-[0-9]{1,3}\Z"))
def test_berth_type_result_is_valid(seat):
    # any accepted seat must have a coach name and a real berth type
    result = berth_type(seat)
    if result is not None:
        coach, berth = result
        assert coach != ""
        assert berth in BERTHS
