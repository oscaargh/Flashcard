from io import StringIO
import argparse

memory_file = StringIO()

parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

def logged_print(*args, **kwargs):
    text = " ".join(map(str, args))
    print(text, **kwargs)  # normal console output
    memory_file.write(text + "\n")


def logged_input(prompt=""):
    response = input(prompt)
    memory_file.write(prompt + response + "\n")
    return response


class FlashcardManager:
    # Manager for all avalible functions in the program
    def __init__(self):
        self.cards = {}
        self.error_counter = {}

    def add_card(self):
        while True:  # outer loop for term
            term = logged_input("The card:\n")
            if term in self.cards:
                logged_print(f"The card \"{term}\" already exists. Try again:")
                continue

            while True:  # inner loop for definition
                definition = logged_input("The definition of the card:\n")
                if definition in self.cards.values():
                    logged_print(f"The definition \"{definition}\" already exists. Try again:")
                    continue

                # valid definition reached
                self.cards[term] = definition
                self.error_counter[term] = 0
                logged_print(f"The pair (\"{term}\":\"{definition}\") has been added.")
                break  # exit inner loop after success

            break  # exit outer loop after success

    def remove_card(self, term):
        if term in self.cards:
            self.cards.pop(term)
            logged_print("The card has been removed.")
        else:
            logged_print(f"Can't remove \"{term}\": there is no such card.")

    def import_card(self):
        file = args.import_from or input("File name:\n")
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for i in range(0, len(lines), 3):
                    term = lines[i].strip()
                    definition = lines[i + 1].strip()
                    error = int(lines[i + 2].strip())
                    self.cards[term] = definition
                    self.error_counter[term] = error
            logged_print(f"{len(lines) // 3} cards have been loaded.")
        except FileNotFoundError:
            logged_print("File not found.")

    def export_card(self):
        file = args.export_to or input("File name:\n")
        with open(file, "w", encoding="utf-8") as f:
            for term, definition in self.cards.items():
                f.write(term + "\n")
                f.write(definition + "\n")
                f.write(str(self.error_counter[term]) + "\n")
            logged_print(f"{len(self.cards)} cards have been saved.")

    def ask_card(self, n):
        import random
        terms = list(self.cards.keys())
        if terms:
            for _ in range(n):
                term = random.choice(terms)  # pick a card (with replacement)
                definition = self.cards[term]
                user_answer = logged_input(f"Print the definition of \"{term}\":\n")
                if user_answer == definition:
                    logged_print("Correct!")
                elif user_answer in self.cards.values():
                    matching_card = next(c for c, defn in self.cards.items() if defn == user_answer)
                    logged_print(
                        f"Wrong. The right answer is \"{definition}\", but your definition is correct for "
                        f"\"{matching_card}\".")
                    self.error_counter[term] += 1
                else:
                    logged_print(f"Wrong. The right answer is \"{definition}\".")
                    self.error_counter[term] += 1

    def log(self, file):
        with open(file, "w", encoding="utf-8")as f:
            f.write(memory_file.getvalue())
            logged_print("The log has been saved.")

    def hardest_card(self):
        if not self.error_counter or max(self.error_counter.values()) == 0:
            logged_print("There are no cards with errors.")
            return

        most_errors = max(self.error_counter.values())
        hardest_cards = [x for x, v in self.error_counter.items() if v == most_errors]
        if len(hardest_cards) == 1:
            logged_print(f"The hardest card is \"{hardest_cards[0]}\". You have {most_errors} errors answering it")
        elif len(hardest_cards) >= 2:
            logged_print(f"The hardest cards are {', '.join(f"\"{card}\"" for card in hardest_cards)}. "
                         f"You have {most_errors} errors answering it")


    def reset_stats(self):
        for key in self.error_counter.keys():
            self.error_counter[key] = 0
        logged_print("Card statistics have been reset.")

    def exit(self):
        if args.export_to:
            with open(args.export_to, "w") as f:
                for term, definition in self.cards.items():
                    f.write(term + "\n")
                    f.write(definition + "\n")
                    f.write(str(self.error_counter[term]) + "\n")
            logged_print(f"{len(self.cards)} cards have been saved.")

class FlashcardApp:
    def __init__(self):
        self.deck = FlashcardManager()

    def run(self):

        if args.import_from:
            self.deck.import_card()

        while True:
            action = logged_input("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n")
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
abc = FlashcardApp()
abc.run()
