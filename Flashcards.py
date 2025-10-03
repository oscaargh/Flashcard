"""
Flashcards App

A command-line flashcards program that allows users to:
- Add, remove, and manage flashcards (term + definition)
- Import/export flashcards to/from files
- Quiz themselves on flashcards
- Track statistics on errors
- Save a log of all actions

Supports command-line arguments:
--import_from : automatically import cards from a file at start
--export_to   : automatically export cards to a file on exit
"""

# ===============================
# Imports and global setup
# ===============================
from io import StringIO
import argparse
from typing import Any

# Memory file for logging all printed output
memory_file = StringIO()

# Create a parser for the handling of command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()


def logged_print(*args: Any, **kwargs: Any) -> None:
    """
    Prints a message to console and also logs it to memory_file.

    Args:
        *args: Values to print
        **kwargs: Optional print keyword arguments (like end, sep)
    """
    text = " ".join(map(str, args))
    print(text, **kwargs)
    memory_file.write(text + "\n")


def logged_input(prompt: str = "") -> str:
    """
    Prompts the user for input, prints prompt to console,
    and logs both the prompt and user's response to memory_file.

    Args:
        prompt (str): Message displayed to the user     
    Returns:
        str: User's input
    """
    response = input(prompt)
    memory_file.write(prompt + response + "\n")
    return response


class FlashcardManager:
    """
    Manages flashcards and their operations:
    - Add, remove, import, export cards
    - Ask user to define cards and track errors
    - Log all console interactions
    - Reset statistics and find hardest cards
    """

    def __init__(self) -> None:
        self.cards: dict[str, str] = {}  # Term:Definition
        # Term:Error_count, i.e. the amount of times a user has incorrectly guessed a card
        self.error_counter: dict[str, int] = {}

    def add_card(self) -> None:
        while True:  # Outer loop for term
            term = logged_input("The card:\n")
            if term in self.cards:
                logged_print(f"The card \"{term}\" already exists. Try again:")
                continue

            while True:  # Inner loop for definition
                definition = logged_input("The definition of the card:\n")
                if definition in self.cards.values():
                    logged_print(
                        f"The definition \"{definition}\" already exists. Try again:")
                    continue

                # Valid definition reached
                self.cards[term] = definition
                self.error_counter[term] = 0
                logged_print(
                    f"The pair (\"{term}\":\"{definition}\") has been added.")
                break  # Exit inner loop after success

            break  # Exit outer loop after success

    def remove_card(self, term: str) -> None:
        if term in self.cards:
            self.cards.pop(term)
            logged_print("The card has been removed.")
        else:
            logged_print(f"Can't remove \"{term}\": there is no such card.")

    def import_card(self) -> None:
        # If no console input in beginning then prompt user for file
        file = args.import_from or input("File name:\n")
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 1st line in file = term, 2nd = definition and 3rd = error count
                for i in range(0, len(lines), 3):
                    term = lines[i].strip()
                    definition = lines[i + 1].strip()
                    error = int(lines[i + 2].strip())
                    self.cards[term] = definition
                    self.error_counter[term] = error
            logged_print(f"{len(lines) // 3} cards have been loaded.")
        except FileNotFoundError:
            logged_print("File not found.")

    def export_card(self) -> None:
        file = args.export_to or input("File name:\n")
        with open(file, "w", encoding="utf-8") as f:
            for term, definition in self.cards.items():
                f.write(term + "\n")
                f.write(definition + "\n")
                f.write(str(self.error_counter[term]) + "\n")
            logged_print(f"{len(self.cards)} cards have been saved.")

    def ask_card(self, n: int) -> None:
        import random
        terms = list(self.cards.keys())
        if terms:  # We can't ask for definitions if we don't have any cards in our dict.
            for _ in range(n):
                term = random.choice(terms)
                definition = self.cards[term]
                user_answer = logged_input(
                    f"Print the definition of \"{term}\":\n")
                if user_answer == definition:
                    logged_print("Correct!")
                elif user_answer in self.cards.values():
                    matching_card = next(
                        c for c, defn in self.cards.items() if defn == user_answer)
                    logged_print(
                        f"Wrong. The right answer is \"{definition}\", but" 
                        "your definition is correct for "
                        f"\"{matching_card}\".")
                    self.error_counter[term] += 1
                else:
                    logged_print(
                        f"Wrong. The right answer is \"{definition}\".")
                    self.error_counter[term] += 1

    def log(self, file: str) -> None:
        with open(file, "w", encoding="utf-8")as f:
            f.write(memory_file.getvalue())
            logged_print("The log has been saved.")

    def hardest_card(self) -> None:
        if not self.error_counter or max(self.error_counter.values()) == 0:
            logged_print("There are no cards with errors.")
            return

        most_errors = max(self.error_counter.values())
        hardest_cards = [k for k, v in self.error_counter.items(
        ) if v == most_errors]  # K = Key, V = Value
        if len(hardest_cards) == 1:
            logged_print(
                f"The hardest card is \"{hardest_cards[0]}\". You have {most_errors} errors answering it"
            )
        elif len(hardest_cards) >= 2:
            names = ', '.join(f'"{card}"' for card in hardest_cards)
            logged_print(
                f"The hardest cards are {names}. "
                f"You have {most_errors} errors answering it"
            )

    def reset_stats(self) -> None:
        for key in self.error_counter.keys():
            self.error_counter[key] = 0
        logged_print("Card statistics have been reset.")

    def exit(self) -> None:
        if args.export_to:  # Automatically exports all the current terms in memory if a CLI argument was given
            with open(args.export_to, "w") as f:
                for term, definition in self.cards.items():
                    f.write(term + "\n")
                    f.write(definition + "\n")
                    f.write(str(self.error_counter[term]) + "\n")
            logged_print(f"{len(self.cards)} cards have been saved.")


class FlashcardApp:
    def __init__(self) -> None:
        self.deck = FlashcardManager()

    def run(self) -> None:

        if args.import_from:
            self.deck.import_card()

        while True:
            action = logged_input(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
            if action == "add":
                self.deck.add_card()
            elif action == "remove":
                card_remove = logged_input("Which card?\n")
                self.deck.remove_card(card_remove)
            elif action == "import":
                self.deck.import_card()
            elif action == "export":
                self.deck.export_card()
            elif action == "ask":
                ask = int(logged_input("How many times to ask?:\n"))
                self.deck.ask_card(ask)
            elif action == "log":
                log = logged_input("File name:\n")
                self.deck.log(log)
            elif action == "hardest card":
                self.deck.hardest_card()
            elif action == "reset stats":
                self.deck.reset_stats()
            elif action == "exit":
                logged_print("bye bye")
                self.deck.exit()
                break


# Run the Flashcards application.
# This creates a FlashcardApp instance and starts the main loop.
abc = FlashcardApp()
abc.run()
