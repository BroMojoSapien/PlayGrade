import tkinter as tk
from tkinter import messagebox
import sqlite3

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
    SELECT id, name, town, fun, safety, cleanliness, shade, seating, bathrooms, parking
    FROM playgrounds
    """)
    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        park_id = row[0]
        name = row[1]
        town = row[2]
        fun = row[3]
        safety = row[4]
        cleanliness = row[5]
        shade = row[6]
        seating = row[7]
        bathrooms = row[8]
        parking = row[9]

        average_score = (fun + safety + cleanliness + shade + seating + bathrooms + parking) / 7
        letter_grade = get_letter_grade(average_score)

        park_listbox.insert(
            tk.END,
            f"{park_id}: {name} - {town} | {average_score:.1f}/10 | Grade: {letter_grade}"
        )

def show_review(event):
    selected = park_listbox.curselection()

    if selected:
        selected_text = park_listbox.get(selected[0])
        park_id = selected_text.split(":")[0]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM playgrounds WHERE id = ?", (park_id,))
        review = cursor.fetchone()

        conn.close()

        details_text.delete("1.0", tk.END)

        if review:
            details_text.insert(tk.END, f"Park: {review[1]}\n")
            details_text.insert(tk.END, f"Town: {review[2]}\n")
            details_text.insert(tk.END, f"Fun: {review[3]}/10\n")
            details_text.insert(tk.END, f"Safety: {review[4]}/10\n")
            details_text.insert(tk.END, f"Cleanliness: {review[5]}/10\n")
            details_text.insert(tk.END, f"Shade: {review[6]}/10\n")
            details_text.insert(tk.END, f"Seating: {review[7]}/10\n")
            details_text.insert(tk.END, f"Bathrooms: {review[8]}/10\n")
            details_text.insert(tk.END, f"Parking: {review[9]}/10\n")
            details_text.insert(tk.END, f"Would Return: {review[11]}\n\n")
            details_text.insert(tk.END, f"Comment:\n{review[10]}")

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
root.geometry("900x800")

title = tk.Label(root, text="PlayGrade", font=("Arial", 22, "bold"))
title.pack(pady=10)

form = tk.Frame(root)
form.pack()

tk.Label(form, text="Park Name").grid(row=0, column=0, sticky="w")
park_name_entry = tk.Entry(form)
park_name_entry.grid(row=0, column=1)

tk.Label(form, text="Town").grid(row=1, column=0, sticky="w")
town_entry = tk.Entry(form)
town_entry.grid(row=1, column=1)

tk.Label(form, text="Fun (1-10)").grid(row=2, column=0, sticky="w")
fun_entry = tk.Entry(form)
fun_entry.grid(row=2, column=1)

tk.Label(form, text="Safety (1-10)").grid(row=3, column=0, sticky="w")
safety_entry = tk.Entry(form)
safety_entry.grid(row=3, column=1)

tk.Label(form, text="Cleanliness (1-10)").grid(row=4, column=0, sticky="w")
cleanliness_entry = tk.Entry(form)
cleanliness_entry.grid(row=4, column=1)

tk.Label(form, text="Shade (1-10)").grid(row=5, column=0, sticky="w")
shade_entry = tk.Entry(form)
shade_entry.grid(row=5, column=1)

tk.Label(form, text="Seating (1-10)").grid(row=6, column=0, sticky="w")
seating_entry = tk.Entry(form)
seating_entry.grid(row=6, column=1)

tk.Label(form, text="Bathrooms (1-10)").grid(row=7, column=0, sticky="w")
bathrooms_entry = tk.Entry(form)
bathrooms_entry.grid(row=7, column=1)

tk.Label(form, text="Parking (1-10)").grid(row=8, column=0, sticky="w")
parking_entry = tk.Entry(form)
parking_entry.grid(row=8, column=1)

tk.Label(form, text="Would Return").grid(row=9, column=0, sticky="w")
return_var = tk.StringVar(value="Yes")
tk.OptionMenu(form, return_var, "Yes", "No", "Maybe").grid(row=9, column=1, sticky="w")

tk.Label(form, text="Comments").grid(row=10, column=0, sticky="nw")
comment_entry = tk.Text(form, height=4, width=30)
comment_entry.grid(row=10, column=1, sticky="w")

tk.Button(root, text="Add Review", command=add_review).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

park_listbox = tk.Listbox(frame, width=40, height=10)
park_listbox.grid(row=0, column=0, padx=10)
park_listbox.bind("<<ListboxSelect>>", show_review)

details_text = tk.Text(frame, width=50, height=15)
details_text.grid(row=0, column=1, padx=10)

tk.Button(root, text="Delete Selected", command=delete_review).pack(pady=5)

load_reviews()

root.mainloop()
