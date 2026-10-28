# Software Engineering Labs: PES1UG24CS083

**Problem Statement #10:** Student Club Event Ticketing & Budget Portal
**Class:** SE Section B | **Faculty:** Dr. Sapna V M
**Actors:** Club Lead, Campus Admin

**Jira Project:** [https://aruukadlabal.atlassian.net/jira/software/c/projects/CEP/boards/34/backlog](https://aruukadlabal.atlassian.net/jira/software/c/projects/CEP/boards/34/backlog)

---

## Lab 1: Requirements Engineering, UML Use-Case Modelling & Component Modelling

**Folder:** [`Lab1_deliverables/`](Lab1_deliverables/)

- `Requirements_Table_PES1UG24CS083.pdf` - **Requirements Table:** 5 FRs + 2 NFRs (Req ID, Type, Description, Priority, Acceptance Criteria, Rationale)
- `UseCase_Diagram_PES1UG24CS083.pdf` - **UML Use-Case Diagram:** actors, use cases, `<<include>>` and `<<extend>>` relations
- `UseCase_Flow_PES1UG24CS083.pdf` - **Use-Case Flow Specification:** preconditions, postconditions, main success scenario, alternate flow
- `Lab3_ComponentModelling_PES1UG24CS083.pdf` - **Component Modelling & Architectural Pattern Selection** (continuation of Lab 1, same problem statement):
  - UML Component Diagram (Layered Architecture): 5 components across Presentation, Business, and Data layers, with 4 required interfaces shown using provided/required (ball-and-socket) notation
  - Architectural Justification: architecture selection, two scenario-specific reasons, one security advantage, one performance benefit (max 1 page)
  - Requirement Traceability: maps every FR-001 to FR-005 and NFR-001 to NFR-002 to the component that satisfies it

## Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Folder:** [`Lab2_deliverables/`](Lab2_deliverables/)

- `Lab2_PES1UG24CS083_SectionB.pdf` - Jira evidence containing:
  - **Backlog:** 3 Epics broken down into 12 User Stories with Fibonacci story points
  - **Sprint 1 & Sprint 2:** Active Sprint boards and Burndown Charts for both completed sprints
  - **Reflection:** answers to the 4 reflection questions on estimation, prioritization, and sprint capacity

**Jira project link:** [https://aruukadlabal.atlassian.net/jira/software/c/projects/CEP/boards/34/backlog](https://aruukadlabal.atlassian.net/jira/software/c/projects/CEP/boards/34/backlog)

## Lab 3: AttendEase - SRS, Software Architecture & Test Plan

**Folder:** [`lab3_deliverables/`](lab3_deliverables/)

- `AttendEase_SRS.pdf` - **Software Requirements Specification**
- `AttendEase_SAD.pdf` - **Software Architecture Document**
- `AttendEase_TestPlan.pdf` - **Test Plan**
- `AttendEase_Combined_SRS_SAD_TestPlan.pdf` - all three documents combined into one file

## Lab 4: LLM-Assisted Debugging & Feature Development (Battleship vs AI)

**Folder:** [`Lab-4/`](Lab-4/)

A terminal Battleship game against a computer opponent, split into separate modules. The original code had a coordinate bug; I fixed it and then added the remaining features with an LLM as a coding assistant, testing each change myself.

**Code:**
- `main.py` - entry point
- `game.py` - turn flow and setup
- `board.py` - ship and shot state
- `ai.py` - computer targeting
- `requirements.txt` - dependency declaration

**Tasks completed (one commit each):**
1. **Consistent coordinate handling** - input, ship placement, player shots and AI shots all use the same coordinate format, so real ship cells register as hits and empty cells as misses
2. **Multi-ship fleet and win logic** - multiple ships, per-ship damage, sunk-ship detection, repeated-shot prevention, and the game ends when the whole fleet is sunk
3. **Smarter AI** - after a hit, the AI targets neighbouring untried cells, never repeats a shot, and handles a board with no cells left
4. **Shot-level feedback** - hit/miss/sunk messages appear exactly once per real shot, with no false messages from the AI's internal candidate selection

**Submission files:**
- `before.mp4` - gameplay before the changes, showing the original bug
- `after.mp4` - gameplay after the changes, showing the fix and new features
- `chat_history.pdf` - complete LLM chat history

**Run it:**
```bash
cd Lab-4
python main.py
```

## Lab 5: Static Code Analysis (Telecom Tower Maintenance Tracker)

**Folder:** [`lab-5/`](lab-5/)

Used **Bandit** (security), **Pylint** (code quality) and **Flake8** (PEP 8 style) to find and fix issues in `tower_maintenance.py`, a maintenance tracker for telecom towers backed by SQLite.

**Results:**

| Tool | Before | After |
|------|--------|-------|
| Bandit | 4 issues (2 Medium, 2 Low) | No issues |
| Pylint | 5.14/10 | 10.00/10 |
| Flake8 | 7 issues | No issues |

The program's output is unchanged: `['Ridge-A'] high 2 1`.

**Key fixes:**
- **SQL injection:** replaced string-formatted SQL with a parameterised query (this also fixed a crash on site names containing an apostrophe, such as `O'Brien`)
- **Unsafe pickle use:** removed the pointless `pickle` round trip in `snapshot()`
- **Hardcoded password:** removed the unused `NOC_PASSWORD` secret from the source code
- **Global state:** moved the database connection and service counter into a `TowerTracker` class
- **Error handling:** narrowed `except Exception` to `sqlite3.Error`, and fixed a crash when checking the risk level of a tower that doesn't exist
- **Style:** snake_case names, docstrings, `if __name__ == "__main__":` guard, and PEP 8 line lengths and spacing

**Files:**
- `tower_maintenance.py` - the cleaned-up script
- `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt` - reports on the original script
- `pylint_report_after.txt`, `bandit_report_after.txt`, `flake8_report_after.txt` - reports after the fixes (the Flake8 report is empty because there are no issues)
- `issues.md` - table of every issue found and how it was fixed
- `reflection.md` - answers to the reflection questions

**Commits:** one per tool, in order: Bandit fixes → Pylint fixes → Flake8 fixes.

**Run it and the tools:**
```bash
cd lab-5
python tower_maintenance.py
pylint tower_maintenance.py
bandit -r tower_maintenance.py
flake8 tower_maintenance.py
```

## Repository Structure

```
SE-Labs-PES1UG24CS083/
├── Lab1_deliverables/
│   ├── README.md
│   ├── Requirements_Table_PES1UG24CS083.pdf
│   ├── UseCase_Diagram_PES1UG24CS083.pdf
│   ├── UseCase_Flow_PES1UG24CS083.pdf
│   └── Lab3_ComponentModelling_PES1UG24CS083.pdf
├── Lab2_deliverables/
│   └── Lab2_PES1UG24CS083_SectionB.pdf
├── lab3_deliverables/
│   ├── AttendEase_SRS.pdf
│   ├── AttendEase_SAD.pdf
│   ├── AttendEase_TestPlan.pdf
│   └── AttendEase_Combined_SRS_SAD_TestPlan.pdf
├── Lab-4/
│   ├── main.py
│   ├── game.py
│   ├── board.py
│   ├── ai.py
│   ├── requirements.txt
│   ├── README.md
│   ├── before.mp4
│   ├── after.mp4
│   └── chat_history.pdf
├── lab-5/
│   ├── tower_maintenance.py
│   ├── pylint_report_before.txt
│   ├── pylint_report_after.txt
│   ├── bandit_report_before.txt
│   ├── bandit_report_after.txt
│   ├── flake8_report_before.txt
│   ├── flake8_report_after.txt
│   ├── issues.md
│   └── reflection.md
└── README.md
```
