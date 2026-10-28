# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The Flake8 issues were the easiest. Long lines, an extra blank line and a missing space around `=` are purely about formatting, so fixing them could not change how the program behaves. Renaming the functions to snake_case and adding docstrings were also simple.

The hardest was removing the `global` statement (Pylint W0603). The counter and the database connection were both module-level variables shared by every function, so there was no one-line fix. I moved them into a `TowerTracker` class, which meant changing every function into a method and updating `main()`, then checking that the output stayed exactly the same. The SQL injection fix was small in code, but it took some thought to see that Pylint's suggestion to use an f-string would have kept the injection problem, and that the real fix was a parameterised query.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Mostly the reports pointed at real problems, but one was misleading. Pylint flagged `service_count` (C0103) for not being an UPPER_CASE constant. It is not a constant at all; it is a counter that changes every time a tower is serviced. Renaming it to `SERVICE_COUNT` would have silenced the warning but made the code more confusing. The real issue was that it was global state, which I fixed by moving it into the class. Bandit's B105 hardcoded password warning was correct, though here the password was not even used, so it was dead code as well as a security risk.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run them automatically so nobody has to remember to. Locally, a pre-commit hook could run Flake8 and Bandit before every commit, so style and security problems are caught before they reach the repository. In continuous integration, for example GitHub Actions, every push and pull request would run all three tools and fail the build if Bandit finds any medium or high severity issue or the Pylint score drops below an agreed level, such as 9.5. Running the tools in my editor would also show warnings while I type, which is the cheapest time to fix them.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** the SQL injection hole is gone and pickle is no longer used, so Bandit now reports no issues.
- **Robustness:** two real bugs were fixed. Adding a site with an apostrophe in its name, such as `O'Brien`, used to crash the program, and asking for the risk level of a tower that does not exist used to crash with a `TypeError`. Errors other than database errors are also no longer silently hidden.
- **Readability:** the code now follows PEP 8 naming, has docstrings that explain each method, and keeps its state inside a class instead of global variables. The Pylint score went from 5.14/10 to 10.00/10 and Flake8 reports no issues.
- **Reusability:** with the `if __name__ == "__main__":` guard, the module can be imported without running the demo.

The program still prints the same result as before, `['Ridge-A'] high 2 1`, so the cleanup did not change its behaviour.
