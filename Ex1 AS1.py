# AI reference: Claude (Anthropic)
# Prompt: "Give comments for each code"
# Used for: writing the explanatory comments throughout this file

import random            # used to generate random numbers and operations
import tkinter as tk     # GUI library
from tkinter import messagebox    #pop-up message boxes

Game_Questions = 10    #number of questions per quiz
First_Try = 2      # points for a correct answer on first try
Second_Try = 1     #points for correct answer on second try
Levels = {1: ("Easy", 1, 10), 2: ("Medium", 10, 100), 3: ("Hard", 100, 1000)}


def randomInt(level):
    """Returns a random integer between 1 and 100."""
    _, low, high = Levels[level]      # Ignoring the name while keeping the range
    return random.randint(low, high)


def decideOperation():
    """Randomly chooses between 1 and 2."""
    return random.choice(["+", "-"])


def isCorrect(userAnswer, correctAnswer):
    """Checks if the answer is correct."""
    return userAnswer == correctAnswer


def getRank(score):
    """Returns the rank of the user."""
    # Maximum possible points
    score = score / (Game_Questions * First_Try) * 100
    if score >= 100:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


class QuizApp:
    """Holds the window and all of the game's status"""
    def __init__(self, root):
        self.root = root
        root.title("A Math Quiz")
        root.geometry("600x300")
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)
        self.level = 1
        self.score = 0
        self.questionNum = 0
        self.attempts = 0
        self.correctAnswer = 0
        self.num1 = self.num2 = 0
        self.operation = "+"
        self.entry = None
        self.feedback = None
        displayMenu(self)


def clearFrame(app):
    for widget in app.frame.winfo_children():
        widget.destroy()


def displayMenu(app):
    """Screen 1 shows up with a difficulty level."""
    clearFrame(app)
    tk.Label(app.frame, text="Difficulty", font=("Arial", 16, "bold")).pack(pady=15)
    for number, (name, _, _) in Levels.items():
        # n=number captures the current value so each button starts its own level
        tk.Button(app.frame, text=f"{number}. {name}", width=20, command=lambda n=number: startQuiz(app, n)).pack(
            pady=5)


def startQuiz(app, level):
    """Reset score and question counter, then begin the first question."""
    app.level = level
    app.score = 0
    app.questionNum = 0
    nextQuestion(app)


def nextQuestion(app):
    """Create a new question, or show results once all questions are done.
    """
    if app.questionNum >= Game_Questions:
        displayResults(app)
        return
    app.questionNum += 1
    app.attempts = 0
    app.num1 = randomInt(app.level)
    app.num2 = randomInt(app.level)
    app.operation = decideOperation()
    # Work out the correct answer in advance
    if app.operation == "+":
        app.correctAnswer = app.num1 + app.num2
    else:
        app.correctAnswer = app.num1 - app.num2
    displayProblem(app)


def displayProblem(app):
    """Screen 2: show the question, an input box and a Submit button."""
    clearFrame(app)
    tk.Label(app.frame, text=f"{app.num1} {app.operation} {app.num2} =", font=("Arial", 22, "bold")).pack(pady=15)
    app.entry = tk.Entry(app.frame, font=("Arial", 16), width=10, justify="center")
    app.entry.pack()
    app.entry.focus()
    app.entry.bind("<Return>", lambda event: submitAnswer(app))
    tk.Button(app.frame, text="Submit", command=lambda:
    submitAnswer(app)).pack(pady=10)
    app.feedback = tk.Label(app.frame, text="", font=("Arial", 15), fg="Black")
    app.feedback.pack()


def submitAnswer(app):
    """Validate the input, mark it, award points and move on."""
    # Input validation: only whole numbers are accepted
    try:
        userAnswer = int(app.entry.get())
    except ValueError:
        app.feedback.config(text="Please enter a number and not letters.")
        return   # does not use up an attempt

    app.attempts += 1
    if isCorrect(userAnswer, app.correctAnswer):
        # 2 points on first try, 1 point on second try
        points = First_Try if app.attempts == 1 else Second_Try
        app.score += points
        messagebox.showinfo("Correct", f"Good Job +{points} points")
        nextQuestion(app)
    elif app.attempts == 1:
        # Wrong first time: give a second chance
        app.feedback.config(text="Try Again.")
        app.entry.delete(0, tk.END)
    else:
        messagebox.showinfo("Incorrect", f"The right answer is {app.correctAnswer}.")
        nextQuestion(app)


def displayResults(app):
    """Final screen: show the rank with Play Again / Quit buttons."""
    clearFrame(app)
    rank = getRank(app.score)
    tk.Label(app.frame, text="Quiz completed", font=("Arial", 16, "bold")).pack(pady=15)
    tk.Label(app.frame, text=f"Rank: {rank}", font=("Arial", 15)).pack(pady=5)
    tk.Button(app.frame, text="Play Again", width=20,
              command=lambda: displayMenu(app)).pack(pady=10)
    tk.Button(app.frame, text="Quit", width=20, command=app.root.destroy).pack()

#Program starts here (only when this file is run directly)
if __name__ == "__main__":
    window = tk.Tk()
    QuizApp(window)
    window.mainloop()
