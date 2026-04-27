import tkinter as tk
from tkinter import messagebox
import json
import os

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

print("WORKING FOLDER:", os.getcwd())

FILE_NAME = "playgrade_reviews.json"

def load_reviews():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_reviews():
    with open(FILE_NAME, "w") as file:
        json.dump(reviews, file, indent=4)

reviews = load_reviews()

def add_review():
    name = park_name_entry.get()
    town = town_entry.get()
    fun = fun_entry.get()
    safety = safety_entry.get()
    cleanliness = cleanliness_entry.get()
    shade = shade_entry.get()
    seating = seating_entry.get()
    bathrooms = bathrooms_entry.get()
    parking = parking_entry.get()
    comment = comment_entry.get("1.0", tk.END).strip()
    would_return = return_var.get()

    if name == "" or town == "":
        messagebox.showwarning("Missing Info", "Please enter park name and town.")
        return

    new_review = {
        "name": name,
        "town": town,
        "fun": fun,
        "safety": safety,
        "cleanliness": cleanliness,
        "shade": shade,
    "seating": seating,
    "bathrooms": bathrooms,
    "parking": parking,
        "comment": comment,
        "would_return": would_return
    }

    reviews.append(new_review)
    save_reviews()
    update_list()
    clear_form()

def update_list():
    park_listbox.delete(0, tk.END)
    for review in reviews:
        park_listbox.insert(tk.END, f'{review["name"]} - {review["town"]}')

def show_review(event):
    selected = park_listbox.curselection()

    if selected:
        index = selected[0]
        review = reviews[index]

        details_text.delete("1.0", tk.END)
        details_text.insert(tk.END, f'Park: {review["name"]}\n')
        details_text.insert(tk.END, f'Town: {review["town"]}\n')
        details_text.insert(tk.END, f'Fun: {review["fun"]}/10\n')
        details_text.insert(tk.END, f'Safety: {review["safety"]}/10\n')
        details_text.insert(tk.END, f'Cleanliness: {review["cleanliness"]}/10\n')
        details_text.insert(tk.END, f'Would Return: {review["would_return"]}\n\n')
        details_text.insert(tk.END, f'Comment:\n{review["comment"]}')

def delete_review():
    selected = park_listbox.curselection()

    if selected:
        index = selected[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this review?")

        if confirm:
            reviews.pop(index)
            save_reviews()
            update_list()
            details_text.delete("1.0", tk.END)
    else:
        messagebox.showwarning("No Selection", "Select a park to delete.")

def clear_form():
    park_name_entry.delete(0, tk.END)
    town_entry.delete(0, tk.END)
    fun_entry.delete(0, tk.END)
    safety_entry.delete(0, tk.END)
    cleanliness_entry.delete(0, tk.END)
    comment_entry.delete("1.0", tk.END)
    return_var.set("Yes")

root = tk.Tk()
root.title("PlayGrade - Yelp for Playgrounds")
root.geometry("900x800")

title = tk.Label(root, text="PlayGrade", font=("Arial", 22, "bold"))
title.pack(pady=10)

form = tk.Frame(root)
form.pack()

tk.Label(form, text="Park Name").grid(row=0, column=0)
park_name_entry = tk.Entry(form)
park_name_entry.grid(row=0, column=1)

tk.Label(form, text="Town").grid(row=1, column=0)
town_entry = tk.Entry(form)
town_entry.grid(row=1, column=1)

tk.Label(form, text="Fun (1-10)").grid(row=2, column=0)
fun_entry = tk.Entry(form)
fun_entry.grid(row=2, column=1)

tk.Label(form, text="Safety (1-10)").grid(row=3, column=0)
safety_entry = tk.Entry(form)
safety_entry.grid(row=3, column=1)

tk.Label(form, text="Cleanliness (1-10)").grid(row=4, column=0)
cleanliness_entry = tk.Entry(form)
cleanliness_entry.grid(row=4, column=1)

tk.Label(form, text="Shade (1-10)"). grid(row=5, column=0)
shade_entry = tk.Entry(form)
shade_entry.grid(row=5, column=1)


tk.Label(form, text="Seating (1-10)").grid(row=6, column=0)
seating_entry = tk.Entry(form)
seating_entry.grid(row=6, column=1)

tk.Label(form, text="Bathrooms (1-10)").grid(row=7, column=0)
bathrooms_entry = tk.Entry(form)
bathrooms_entry.grid(row=7, column=1)

tk.Label(form, text="Parking (1-10)").grid(row=8, column=0)
parking_entry = tk.Entry(form)
parking_entry .grid(row=8, column=1)

tk.Label(form, text="Would Return").grid(row=9, column=0, sticky="w")
return_var = tk.StringVar(value="Yes")
tk.OptionMenu(form, return_var, "Yes", "No", "Maybe").grid(row=9, column=1, sticky="w")

tk.Label(form, text="Comments").grid(row=10, column=0, sticky="nw")
comment_entry = tk.Text(form, height=4, width=25)
comment_entry.grid(row=10, column=1, sticky="w")

tk.Button(root, text="Add Review", command=add_review).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

park_listbox = tk.Listbox(frame, width=30)
park_listbox.grid(row=0, column=0)
park_listbox.bind("<<ListboxSelect>>", show_review)

details_text = tk.Text(frame, width=40)
details_text.grid(row=0, column=1)

tk.Button(root, text="Delete Selected", command=delete_review).pack(pady=5)

update_list()

root.mainloop()

