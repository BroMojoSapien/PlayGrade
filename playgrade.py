import tkinter as tk
from tkinter import messagebox
import sqlite3

from PIL import Image, ImageTk

DB_NAME = "playgrade.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playgrounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        town TEXT,
        fun INTEGER,
        safety INTEGER,
        cleanliness INTEGER,
        shade INTEGER,
        seating INTEGER,
        bathrooms INTEGER,
        parking INTEGER,
        comment TEXT,
        would_return TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_letter_grade(score):
    if score >= 9:
        return "A"
    elif score >= 8:
        return "B"
    elif score >= 7:
        return "C"
    elif score >= 6:
        return "D"
    else:
        return "F"

def add_review():
    name = park_name_entry.get()
    town = town_entry.get()

    try:
    	fun = int(fun_entry.get())
    	safety = int(safety_entry.get())
    	cleanliness = int(cleanliness_entry.get())
    	shade = int(shade_entry.get())
    	seating = int(seating_entry.get())
    	bathrooms = int(bathrooms_entry.get())
    	parking = int(parking_entry.get())
    except:
    	messagebox.showwarning("Invalid Input", "All ratings must be numbers.")
    	return

    comment = comment_entry.get("1.0", tk.END).strip()
    would_return = return_var.get()
    average_score = (fun + safety + cleanliness + shade + seating + bathrooms + parking) / 7
    letter_grade = get_letter_grade(average_score)

    if name == "" or town == "":
    	messagebox.showwarning("Missing Info", "Please enter park name and town.")
    	return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO playgrounds (
        name, town, fun, safety, cleanliness, shade,
        seating, bathrooms, parking, comment, would_return
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, town, fun, safety, cleanliness, shade,
        seating, bathrooms, parking, comment, would_return
    ))

    conn.commit()
    conn.close()

    clear_form()
    load_reviews()

def load_reviews():
    park_listbox.delete(0, tk.END)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        town,
        AVG(fun),
        AVG(safety),
        AVG(cleanliness),
        AVG(shade),
        AVG(seating),
        AVG(bathrooms),
        AVG(parking),
        COUNT(*)
    FROM playgrounds
    GROUP BY name, town
    """)
    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        name = row[0]
        town = row[1]
        fun = row[2]
        safety = row[3]
        cleanliness = row[4]
        shade = row[5]
        seating = row[6]
        bathrooms = row[7]
        parking = row[8]
        review_count = row[9]

        average_score = (fun + safety + cleanliness + shade + seating + bathrooms + parking) / 7
        letter_grade = get_letter_grade(average_score)

        park_listbox.insert(
            tk.END,
            f"{name} - {town} | {average_score:.1f}/10 | Grade: {letter_grade} | {review_count} reviews"
        )

def show_review():
    selected = park_listbox.curselection()

    if not  selected:
        details_text.delete("1.0", tk.END)
        details_text.insert(tk.END, "Nothing Selected")
        return

    selected_text = park_listbox.get(selected[0])

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, selected_text)


def delete_review():
    selected = park_listbox.curselection()

    if selected:
        selected_text = park_listbox.get(selected[0])
        park_id = selected_text.split(":")[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this review?"
        )

        if confirm:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM playgrounds WHERE id = ?", (park_id,))

            conn.commit()
            conn.close()

            details_text.delete("1.0", tk.END)
            load_reviews()
    else:
        messagebox.showwarning("No Selection", "Select a park to delete.")

def clear_form():
    park_name_entry.delete(0, tk.END)
    town_entry.delete(0, tk.END)
    fun_entry.delete(0, tk.END)
    safety_entry.delete(0, tk.END)
    cleanliness_entry.delete(0, tk.END)
    shade_entry.delete(0, tk.END)
    seating_entry.delete(0, tk.END)
    bathrooms_entry.delete(0, tk.END)
    parking_entry.delete(0, tk.END)
    comment_entry.delete("1.0", tk.END)
    return_var.set("Yes")

setup_db()

root = tk.Tk()
root.title("PlayGrade - Yelp for Playgrounds")
root.geometry("1000x1000")
root.configure(bg="white")

canvas = tk.Canvas(root, bg="white")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

canvas.create_window((400, 0), window=scrollable_frame, anchor="n")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
canvas.configure(width=800)
scrollbar.pack(side="right", fill="y")

logo = tk.PhotoImage(file="playgrade_logo_clean.png")
logo = logo.subsample(1, 1)

logo_label = tk.Label(scrollable_frame, image=logo, bg="white")
logo_label.image = logo
logo_label.pack(pady=10)

title = tk.Label(scrollable_frame, bg="white",  text="PlayGrade", font=("Arial", 22, "bold"))
title.pack(pady=10)

form = tk.Frame(scrollable_frame, bg="white")
form.pack(pady=10)

frame = tk.Frame(scrollable_frame, bg="white")
frame.pack(pady=20)

tk.Label(form, text="Park Name", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
park_name_entry = tk.Entry(form)
park_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form, text="Town", bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
town_entry = tk.Entry(form)
town_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form, text="Fun (1-10)", bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
fun_entry = tk.Entry(form)
fun_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(form, text="Safety (1-10)", bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
safety_entry = tk.Entry(form)
safety_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(form, text="Cleanliness (1-10)", bg="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
cleanliness_entry = tk.Entry(form)
cleanliness_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(form, text="Shade (1-10)", bg="white").grid(row=5, column=0, sticky="w", padx=10, pady=5)
shade_entry = tk.Entry(form)
shade_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(form, text="Seating (1-10)", bg="white").grid(row=6, column=0, sticky="w", padx=10, pady=5)
seating_entry = tk.Entry(form)
seating_entry.grid(row=6, column=1, padx=10, pady=5)

tk.Label(form, text="Bathrooms (1-10)", bg="white").grid(row=7, column=0, sticky="w", padx=10, pady=5)
bathrooms_entry = tk.Entry(form)
bathrooms_entry.grid(row=7, column=1, padx=10, pady=5)

tk.Label(form, text="Parking (1-10)", bg="white").grid(row=8, column=0, sticky="w", padx=10, pady=5)
parking_entry = tk.Entry(form)
parking_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Label(form, text="Would Return", bg="white").grid(row=9, column=0, sticky="w", padx=10, pady=5)
return_var = tk.StringVar(value="Yes")
tk.OptionMenu(form, return_var, "Yes", "No", "Maybe").grid(row=9, column=1, sticky="w")

tk.Label(form, text="Comments", bg="white").grid(row=10, column=0, sticky="nw")
comment_entry = tk.Text(form, height=4, width=30)
comment_entry.grid(row=10, column=1, sticky="w")

tk.Button(scrollable_frame, text="Add Review", bg="white",  command=add_review).pack(pady=5)

frame = tk.Frame(scrollable_frame, bg="white")
frame.pack(pady=10)

tk.Label(frame, text="Parks and Playgrounds", bg="white", font=("Arial", 14, "bold")).pack(pady=5)
park_listbox = tk.Listbox(frame, width=80, height=4)
park_listbox.pack(pady=10)

details_text = tk.Text(frame, width=80, height=4, wrap="word")
details_text.pack(pady=10)

park_listbox.bind("<<ListboxSelect>>", lambda e: show_review())

tk.Button(scrollable_frame, text="Delete Selected", command=delete_review).pack(pady=5)

load_reviews()

root.mainloop()
