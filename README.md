# Flashcards App

A command-line flashcards program to create, manage, and quiz yourself on flashcards. Tracks mistakes and can log all actions.

---

## Features

* Add, remove, and manage flashcards
* Import/export cards from/to files
* Quiz yourself multiple times
* Track mistakes per card and identify the hardest cards
* Reset statistics or save session logs
* Optional command-line arguments: `--import_from` and `--export_to`

## Usage

Run the program:

```bash
python Flashcards.py
```

With optional command-line arguments:

```bash
python Flashcards.py --import_from="cards.txt" --export_to="cards.txt"
```

---

## Commands

| Command        | Description                   |
| -------------- | ----------------------------- |
| `add`          | Add a new flashcard           |
| `remove`       | Remove a flashcard by term    |
| `import`       | Import flashcards from a file |
| `export`       | Export flashcards to a file   |
| `ask`          | Quiz yourself on cards        |
| `log`          | Save console interaction log  |
| `hardest card` | Show cards with most mistakes |
| `reset stats`  | Reset all mistake counters    |
| `exit`         | Exit the program              |

---

## File Format

Each flashcard is stored as **three lines**:

```
Term
Definition
Number of mistakes
```

Example:

```
Python
A programming language
2
Java
Another programming language
0
```

---

## Example Session

```text
Input the action:
> add
The card:
> Python
The definition of the card:
> A programming language
The pair ("Python":"A programming language") has been added.
```

---

