# Lab 5: Issues Found and Fixed

Script: `tower_maintenance.py`. Line numbers refer to the original file.

## Summary

| Tool | Before | After |
|------|--------|-------|
| Bandit | 4 issues (2 Medium, 2 Low) | No issues |
| Pylint | 5.14/10 | 10.00/10 |
| Flake8 | 7 issues | No issues |

The program's output is the same before and after: `['Ridge-A'] high 2 1`.

## Issue table

High and medium severity issues are listed first.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | SQL injection (Bandit B608, Medium) | Security | 11 | The INSERT query is built with `%` string formatting, so the site name goes straight into the SQL. A name containing a quote changes the query. It is also a real bug: adding a site called `O'Brien` crashes with `sqlite3.OperationalError`. | Use a parameterised query with `?` placeholders and pass the values as a tuple, so SQLite treats them as data, never as SQL. |
| 2 | Unsafe deserialisation with pickle (Bandit B301, Medium) | Security | 43 | `snapshot()` round-trips the rows through `pickle.dumps` and `pickle.loads`. `pickle.loads` can run arbitrary code if it is ever given untrusted data, and here the round trip does nothing useful. | Return `list(...)` of the fetched rows instead, which gives the same copy without pickle. |
| 3 | Importing pickle (Bandit B403, Low) | Security | 1 | The pickle module is imported, which Bandit flags as a risk. | Removed the import once `snapshot()` no longer needed it. |
| 4 | Hardcoded password (Bandit B105, Low) | Security | 6 | `NOC_PASSWORD = "tower-noc-77"` stores a secret in the source code, where anyone with the code can read it. It was never used. | Removed the variable. If it is needed later, it should be read from an environment variable rather than written in the code. |
| 5 | Global variable modified inside a function (Pylint W0603) | Code quality | 7, 16 | `serviceTower` uses `global service_count`. Global state is hard to follow and test, and the database connection was also global. | Moved the connection and the counter into a `TowerTracker` class, so the state belongs to an object instead of the module. |
| 6 | Catching a too-general exception (Pylint W0718) | Bug risk | 20 | `except Exception` catches every error, including programming mistakes, and hides them behind "service failed". | Catch only `sqlite3.Error`, the database errors this code expects. |
| 7 | Crash on unknown tower id | Bug | 35–36 | `riskLevel` reads `row[0]` without checking whether the tower exists. For an unknown id `fetchone()` returns `None` and the program crashes with a `TypeError`. | Check for `None` and return `"unknown"`. |
| 8 | Unnecessary `else` after `return` (Pylint R1705) | Code quality | 36–39 | The `else` adds an extra level of indentation for no reason. | Removed the `else` and returned `"normal"` directly. |
| 9 | Function names not in snake_case (Pylint C0103) | Style | 10, 15, 34 | `addTower`, `serviceTower` and `riskLevel` use camelCase, which goes against PEP 8. | Renamed them to `add_tower`, `service_tower` and `risk_level`. |
| 10 | Module-level variable named like a constant (Pylint C0103) | Style | 7 | `service_count` sits at module level, so Pylint expects an UPPER_CASE constant, but it is really a changing counter. | Fixed by making it the `self.service_count` attribute of `TowerTracker` (see #5). |
| 11 | Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 10, 15, 25, 34, 42, 46 | The module and none of the functions had docstrings explaining what they do. | Added a module docstring, a class docstring and a docstring for every method and `main()`. |
| 12 | Old-style `%` string formatting (Pylint C0209) | Style | 11 | Pylint suggests an f-string instead of `%` formatting. | Removed by the fix for #1: the query no longer formats strings at all, which is the correct fix here (an f-string would still allow SQL injection). |
| 13 | Code runs on import | Code quality | 54 | `main()` is called at the bottom of the file, so importing the module runs the demo. | Wrapped the call in `if __name__ == "__main__":`. |
| 14 | Lines too long (Flake8 E501, Pylint C0301) | Style | 5, 11, 18, 35, 43 | Several lines were longer than 79 characters (up to 120). | Split long SQL strings and calls across lines inside brackets. |
| 15 | Too many blank lines (Flake8 E303) | Style | 22–25 | Three blank lines before `overdue`; PEP 8 allows two between top-level definitions. | Removed the extra blank line. |
| 16 | Missing whitespace around operator (Flake8 E225) | Style | 50 | `total=len(snapshot())` has no spaces around `=`. | Changed to `total = len(...)`. |

## Commits

1. **Bandit fixes:** issues 1–4.
2. **Pylint fixes:** issues 5–13, plus the lines over Pylint's 100-character limit (part of #14).
3. **Flake8 fixes:** issues 14–16, wrapping the remaining lines to Flake8's 79-character limit.
