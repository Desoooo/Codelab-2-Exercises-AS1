# AI reference: Claude (Anthropic)
# Prompt: "Give comments for each code"
# Used for: writing the explanatory comments throughout this file
# and identifying an indentation bug in showRecords (see note below)

from tkinter import *
from tkinter import messagebox, simpledialog

FILE_NAME = "studentMarks.txt" # data file: first line = count, then one student per line
Max_Marks = 160                # 3 coursework marks (3 x 20) + exam (100)

root = Tk()
root.title("Student Manager")
root.geometry("700x500")

# Each student is a list: [code, name, cw1, cw2, cw3, exam]
students = []

# Top frame holds the menu buttons
menuframe = Frame(root)
menuframe.pack(side=TOP, pady=5)

# Canvas + scrollbar so long record lists can be scrolled
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Frame inside the canvas where the records are drawn
recordsframe = Frame(canvas)
canvas.create_window(0,0, window=recordsframe, anchor=NW)
recordsframe.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def readFile():
    students.clear()
    with open(FILE_NAME, "r") as file:
        for line_number, line in enumerate(file, start=1):
            if line_number > 1 and line.strip():
                parts = line.strip().split(",")
                try:
                    # Convert numbers to int; keep the name as text
                    student = [int(parts[0]), parts[1].strip(), int(parts[2].strip()), int(parts[3].strip()),
                               int(parts[4].strip()), int(parts[5].strip())]
                except (ValueError, IndexError):
                    continue  # skip any badly formatted line
                students.append(student)







def saveFile():
    with open(FILE_NAME, "w") as file:
        file.write(str(len(students)) + "\n")
        for s in students:
            file.write(",".join(str(item) for item in s)+ "\n")

# ---------- Calculation help ----------
def coursework(s):
    """Total of the three coursework marks (out of 60)."""
    return s[2] + s[3] + s[4]

def overall(s):
    """Coursework plus exam (out of 160)."""
    return coursework(s) + s[5]

def percents(s):
    """Overall mark as a percentage."""
    return overall(s) / Max_Marks * 100

def grade(p):
    """Convert a percentage into a letter grade."""
    if p >= 70:
        return "A"
    if p >= 60:
        return "B"
    if p >= 50:
        return "C"
    if p >= 40:
        return "D"
    return "F"

# ---------- Display Page----------
def clearRecords():
    """Remove old records from the screen before drawing new ones."""
    for widget in recordsframe.winfo_children():
        widget.destroy()

# Fix: this loop was indented inside the heading loop, so only the last
# student was displayed. It now sits at the correct level.

def showRecords(studentList, showSummary=False):
    """Draw a table of the given students; optionally add a summary line."""
    clearRecords()
    headings = ["Name", "Number", "Coursework /60", "Exam /100", "Percentage", "Grade"]
    for col, heading in enumerate(headings):
        Label(recordsframe, text=heading, width=20, font =("Arial", 15, "bold")).grid(row=0, column=col)
        for i, s in enumerate(studentList, start=1):
            p = percents(s)
        values = [s[1], s[0], coursework(s), s[5], f"{p:.1f}%", grade(p)]
        for col, value in enumerate(values):
            Label(recordsframe, text=value, width=20).grid(row=i, column=col)

    if showSummary and studentList:
        average = sum(percents(s) for s in studentList) / len(studentList)
        Label(recordsframe, font=("Arial", 15, "bold"), text=f"Number of students: {len(studentList)} Average percentage: {average:.1f}%").grid(row=len(studentList) + 2, column=0, columnspan=6, pady=10)

def findStudent(query):
    query = query.strip().lower()
    for s in students:
        if str(s[0]) == query or s[1].lower() == query:
            return s
    return None

def askStudent():
    """Ask the user for a name/ID and return the matching student."""
    query = simpledialog.askstring("Select a Student.", "Enter the student's name or ID:")
    if query is None:
        return None
    student = findStudent(query)
    if student is None:
        messagebox.showinfo("Error not found", "No student matches the details you have input.")
    return student

# ---------- Menu actions ----------
def viewAll():
    showRecords(students, showSummary=True)

def viewOne():
    student = askStudent()
    if student:
        showRecords([student])

def showHighest():
    if students:
        showRecords([max(students, key=overall)])

def showLowest():
    if students:
        showRecords([min(students, key=overall)])

def sortRecord():
    highestFirst = messagebox.askyesno("Sort", "Would you like to see te highest first?\n\nYes = descending, No = ascending")
    showRecords(sorted(students, key=overall, reverse=highestFirst), showSummary=True)

def addStudent():
    code = simpledialog.askinteger("Add Student", "Student code (1000-9999):", minvalue=1000, maxvalue=9999)
    if code is None:
        return
    if findStudent(str(code)):
        messagebox.showerror("Duplicate", "Student already exists. Please try again.")
        return
    name = simpledialog.askstring("Add Student", "Student name:")
    if not name or not name.strip():
        return
    marks = []
    for i in range(1,4):
        mark = simpledialog.askinteger("Add student", f"Coursework mark {i} (0-20):", minvalue=0, maxvalue=20)
        if mark is None:
            return
        marks.append(mark)
    exam = simpledialog.askinteger("Add student", "Exam mark (0-100):", minvalue=0, maxvalue=100)
    if exam is None:
        return
    student = [code, name.strip()] + marks + [exam]
    students.append(student)
    saveFile()
    showRecords([student])

def deleteStudent():
    student = askStudent()
    if student and messagebox.askyesno("Confirm", f"Delete {student[1]}?"):
        students.remove(student)
        saveFile()
        showRecords(students, showSummary=True)

def updateStudent():
    student = askStudent()
    if not student:
        return
    choice = simpledialog.askinteger(
        "Update Student",
        "Which item would you like to update?\n1 Name\n2 Coursework mark1\n" "3 Coursework mark2\n4 Coursework mark 3\n5 Exam mark", minvalue=1, maxvalue=5)
    if choice is None:
        return
    if choice == 1:
        newName= simpledialog.askstring("Update student", "New name:")
        if not newName or not newName.strip():
            return
        student[1] = newName.strip()
    else:
        limit = 100 if choice == 5 else 20
        newMark = simpledialog.askinteger("Update student", f"New mark (0-{limit}):", minvalue=0, maxvalue=limit)
        if newMark is None:
            return
        student[choice] = newMark
    saveFile()
    showRecords([student])

buttons = [
    ("1. View all records", viewAll),
    ("2. View one record", viewOne),
    ("3. View Highest record", showHighest),
    ("4. View Lowest record", showLowest),
    ("5. Sort records", sortRecord),
    ("6. Add a student", addStudent),
    ("7. Delete a Student", deleteStudent),
    ("8. Update student record", updateStudent),
]
for i, (text, command) in enumerate(buttons):
    Button(menuframe, text=text, width=20, command=command).grid(row=i // 4, column=i % 4, padx=5, pady=5)

# ---------- Program start ----------
try:
    readFile()
except FileNotFoundError:
    messagebox.showerror("File not found", f"Could not find:\n{FILE_NAME}")
else:
    showRecords(students, showSummary=True)

root.mainloop()

