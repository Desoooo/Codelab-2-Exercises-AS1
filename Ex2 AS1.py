# Exercise 2: Alexa-style Joke Assistant (Tkinter GUI)
# Loads jokes from randomJokes.txt (setup punchline on each line),
# shows a random setup, and reveals the punchline on button click.

import os
import random
import tkinter as tk
from tkinter import messagebox

JOKES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'randomJokes.txt')


def loadJokes(path):
    """Read the file and return a list of (setup, punchline) tuples."""
    jokes = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:  # remove spaces and newline characters
            line = line.strip() # skip blank or badly formatted lines
            if "?" not in line:
                continue
                # Split only at the FIRST question mark: setup before it, punchline after it
            setup, punchline = line.split("?", 1)
            # Put the question mark back on the setup
            jokes.append((setup.strip() + "?", punchline.strip()))
    return jokes


class JokeApp:
    """Builds the window and handles the button actions."""
    def __init__(self, root, jokes):
        self.root = root
        self.jokes = jokes
        self.current = None

        root.title("Joker Assistant")
        root.geometry("400x400")

        # Red label for the setup, blue label for the punchline (wraps long text)

        self.setupLabel = tk.Label(root, text="", wraplength=380, font=("Arial", 15), fg="red")
        self.setupLabel.pack(pady=5)
        self.punchLabel = tk.Label(root, text="", wraplength=380, font=("Arial", 15), fg="blue")
        self.punchLabel.pack(pady=5)

        # Buttons: Show Punchline and Next Joke start disabled until a joke is told
        self.tellButton = tk.Button(root, text="Alexa tell me a joke", width=20, command=self.newJoke)
        self.tellButton.pack(pady=5)
        self.punchButton = tk.Button(root, text="Show Punchline", width=20, state="disabled",
                                     command=self.showPunchline)
        self.punchButton.pack(pady=5)
        self.nextButton = tk.Button(root, text="Now for the next Joke", width=22, state="disabled",
                                    command=self.newJoke)
        self.nextButton.pack(pady=5)
        tk.Button(root, text="Quit", width=20, command=root.destroy).pack(pady=5)

    # These two methods must be indented so they sit INSIDE the class
    def newJoke(self):
        self.current = random.choice(self.jokes)
        self.setupLabel.config(text=self.current[0])
        self.punchLabel.config(text="")
        self.punchButton.config(state="normal")
        self.nextButton.config(state="normal")

    def showPunchline(self):
        if self.current:
            self.punchLabel.config(text=self.current[1])

# Program starts here
if __name__ == "__main__":
    window = tk.Tk()
    # Error handling: stop politely if the file is missing
    try:
        jokeList = loadJokes(JOKES_FILE)
    except FileNotFoundError:
        messagebox.showerror("Error file not found", f"Could not find the file:\n{JOKES_FILE}")
        window.destroy()
        raise SystemExit
    # Error handling: stop politely if the file has no usable jokes
    if not jokeList:
        messagebox.showerror("Error no jokes", "The joke file has no lines")
        window.destroy()
        raise SystemExit
    JokeApp(window, jokeList)
    window.mainloop()