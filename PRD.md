# PRD: Job Application Tracker

## Problem
Finding a job is hard enough as it is and keeping track of every application with a lack of organisation makes it worse.

## Goals
- Allows a job application to be added in under 10 seconds
- Enables User to see current state of each application
- Lets the User move through a pipeline (applied - interviewing - offered/rejected) and filtered by status or company

## Non-goals
- No GUI or web interface
- No multi-user support or cloud sync
- No job board integration


## MVP features
1. Add an application — company, role, source, link, status defaults to "applied"
2. List all applications in a table
3. Update an application's status by id
4. Archive an application without deleting its history
5. Filter applications by status and/or company


## Tech stack
 Language: Python — Why: strong CLI ergonomics (Typer), and sqlite3 is built into the standard library
- Key libraries: Typer (CLI commands from type hints), Rich (table output), pytest (testing) — Why: minimal boilerplate, well-documented, widely used
- Storage: SQLite, single local file — Why: a real relational database with transactions and constraints, without running a separate server

## Success criteria
- I can add, update, archive, and filter my real job applications through the CLI for at least two weeks without going back to a spreadsheet
- Test suite (test_db.py, test_cli.py) passes and covers empty-database, missing-id, and filter-combination edge cases
- Installable as a real command via `pip install -e .`, so `pipeline list` works directly in the terminal
