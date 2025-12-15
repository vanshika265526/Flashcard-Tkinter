import tkinter as tk
import csv
import random

# --- Load flashcards from CSV ---
flashcards = []

try:
    with open("flashcards.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Add an initial weight for spaced repetition
            flashcards.append({"question": row["question"], "answer": row["answer"], "weight": 1})
except FileNotFoundError:
    print("flashcards.csv not found! Make sure it is in the same folder as this script.")
    exit()

# --- Global variables ---
current_card = {}
flipping = False

# --- Functions ---
def pick_card():
    global current_card
    # Weighted random selection
    total_weight = sum(card["weight"] for card in flashcards)
    r = random.uniform(0, total_weight)
    upto = 0
    for card in flashcards:
        if upto + card["weight"] >= r:
            current_card = card
            break
        upto += card["weight"]
    question_label.config(text=current_card["question"])
    answer_label.config(text="")

def animate_flip(showing_answer):
    global flipping
    flipping = True
    steps = 10
    def shrink(step):
        if step > 0:
            question_label.config(width=25 - step*2)
            root.after(30, shrink, step-1)
        else:
            # Swap text
            if showing_answer:
                question_label.config(text=current_card["answer"])
            else:
                question_label.config(text=current_card["question"])
            grow(0)

    def grow(step):
        if step < steps:
            question_label.config(width=step*2 + 5)
            root.after(30, grow, step+1)
        else:
            global flipping
            flipping = False

    shrink(steps)

def flip_card():
    if not flipping:
        animate_flip(True)

def mark_easy():
    current_card["weight"] = max(1, current_card["weight"] - 1)
    pick_card()

def mark_hard():
    current_card["weight"] += 2
    pick_card()

def mark_forgot():
    current_card["weight"] += 5
    pick_card()

# --- GUI ---
root = tk.Tk()
root.title("Animated Flashcard App")
root.geometry("600x400")  # Wider window for long text

# Question / Answer Label
question_label = tk.Label(
    root, text="", font=("Arial", 18), relief="raised", bg="white", 
    wraplength=550, justify="center", padx=10, pady=20
)
question_label.pack(pady=30, fill="both", expand=True)

answer_label = tk.Label(
    root, text="", font=("Arial", 16), fg="blue", wraplength=550, justify="center"
)
answer_label.pack(pady=10)

# Buttons
btn_frame1 = tk.Frame(root)
btn_frame1.pack(pady=10)

flip_btn = tk.Button(btn_frame1, text="Flip Card", width=12, command=flip_card)
flip_btn.grid(row=0, column=0, padx=10)

next_btn = tk.Button(btn_frame1, text="Next Card", width=12, command=pick_card)
next_btn.grid(row=0, column=1, padx=10)

btn_frame2 = tk.Frame(root)
btn_frame2.pack(pady=10)

easy_btn = tk.Button(btn_frame2, text="Easy", width=10, command=mark_easy)
easy_btn.grid(row=0, column=0, padx=5)

hard_btn = tk.Button(btn_frame2, text="Hard", width=10, command=mark_hard)
hard_btn.grid(row=0, column=1, padx=5)

forgot_btn = tk.Button(btn_frame2, text="Forgot", width=10, command=mark_forgot)
forgot_btn.grid(row=0, column=2, padx=5)

pick_card()  # Show the first card

root.mainloop()
