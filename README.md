Collecting workspace information# Books — Project Overview

A small Tkinter-based desktop app to manage books, authors and publishers using a local SQLite database.

## Structure
- bookdb.py — database access layer (SQLite).
- gui.py — Tkinter UI and dialog classes.
- main.py — program entry point.
- pyproject.toml — project metadata.
- .python-version — pinned Python version.
- .gitignore — ignored files.
- README.md — project README (this file complements it).

## How to run
Run the app with Python 3.12+:
```sh
python3 main.py
```

or

```sh
uv run main.py
```


The entry point is [`main.main`](main.py), which calls [`gui.start_gui`](gui.py).

## Database
The app uses SQLite with a database file named in `bookdb.books_db` (books.db). Schema is expected to contain tables:
- books (id, author, publisher, isbn, edition, title)
- authors (id, name)
- publishers (id, name)

All data access is in bookdb.py. Key functions:
- `bookdb.get_books` — fetch all books.
- `bookdb.get_book` — fetch a single book by id.
- `bookdb.get_authors` — fetch authors.
- `bookdb.get_publishers` — fetch publishers.
- `bookdb.save_book` — insert/update a book.
- `bookdb.save_author` — insert/update an author.
- `bookdb.save_publisher` — insert/update a publisher.
- `bookdb.delete_book` — delete a book.
- `bookdb.delete_author` — delete an author.
- `bookdb.delete_publisher` — delete a publisher.

## User interface
Implemented in gui.py. Main components:
- `gui.Application` — main window with three tabs (Books, Publishers, Authors).
- `gui.EditBookDlg` — dialog to create/edit books.
- `gui.EditAuthorDlg` — dialog to create/edit authors.
- `gui.EditPublisherDlg` — dialog to create/edit publishers.
- `gui.get_key` — helper to lookup dictionary key by value.
- [`gui.start_gui`](gui.py) — convenience function to start the UI (called by [`main.main`](main.py)).

UI behaviour:
- Lists are shown with `ttk.Treeview`.
- Items can be created, edited, deleted; dialogs call the corresponding `bookdb` save/delete functions and refresh the tables.

## Notes & tips
- No external dependencies are declared in pyproject.toml.
- Ensure books.db exists and has the expected tables before running. (se **sql/create_books.sql**)
- Python version is pinned in .python-version.
- To extend: add input validation, error handling around DB operations, or package into a GUI installer.

References:
- Source files: bookdb.py, gui.py, main.py, pyproject.toml, .python-version, .gitignore, README.md.