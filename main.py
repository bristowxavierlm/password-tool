import tkinter as tk
from tkinter import messagebox, filedialog
from zxcvbn import zxcvbn

# Analyze password strength
def analyze_password(password):
    result = zxcvbn(password)
    score = result['score']
    time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    feedback = result['feedback']
    return score, time, feedback

# Leetspeak helper
def leetspeak(word):
    leet_dict = {'a':'@', 'e':'3', 'i':'1', 'o':'0', 's':'$', 't':'7'}
    return ''.join(leet_dict.get(c.lower(), c) for c in word)

# Wordlist generation
def generate_variations(inputs):
    variants = set()
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    for word in inputs:
        if not word: continue
        variants.update([word, word.lower(), word.capitalize(), leetspeak(word)])
        for year in years:
            variants.add(word + year)
            variants.add(leetspeak(word) + year)
    return sorted(variants)

# Save wordlist
def export_wordlist(words):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "w") as f:
            for word in words:
                f.write(word + "\n")
        messagebox.showinfo("Exported", f"✅ Wordlist saved to:\n{filepath}")

# GUI handlers
def on_analyze():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Missing", "Please enter a password.")
        return

    score, time, feedback = analyze_password(password)

    # Update strength bar
    strength_colors = {
        0: "#8B0000",  # Dark Red
        1: "#FF6347",  # Light Red
        2: "#FFA500",  # Orange
        3: "#90EE90",  # Light Green
        4: "#006400",  # Dark Green
    }
    bar_width = (score + 1) * 60
    canvas_strength.coords(strength_bar, 0, 0, bar_width, 20)
    canvas_strength.itemconfig(strength_bar, fill=strength_colors[score])

    # Show text result
    result_text = f"🔐 Score: {score}/4\n⏱ Crack Time: {time}"
    if feedback["warning"]:
        result_text += f"\n⚠️ {feedback['warning']}"
    if feedback["suggestions"]:
        result_text += "\n💡 " + " ".join(feedback["suggestions"])
    lbl_result.config(text=result_text)


def on_generate_wordlist():
    fields = [
entry_fields[key].get().strip() for key in entry_fields
    ]
    if not any(fields):
        messagebox.showwarning("Missing", "Fill at least one field.")
        return

    wordlist = generate_variations(fields)
    export_wordlist(wordlist)

# ---------------- GUI Setup ---------------- #
root = tk.Tk()
root.title("🔐 Password Tool")
root.geometry("440x580")
root.resizable(False, False)
root.configure(bg="#f8f8f8")

tk.Label(root, text="Enter Password:", bg="#f8f8f8").pack(pady=(15, 0))
entry_password = tk.Entry(root, show="*", width=30)
entry_password.pack(pady=5)

# Strength Meter Canvas
canvas_strength = tk.Canvas(root, width=300, height=20, bg="#ddd", highlightthickness=0)
canvas_strength.pack(pady=(0, 10))
strength_bar = canvas_strength.create_rectangle(0, 0, 0, 20, fill="gray")


tk.Button(root, text="Analyze Strength", command=on_analyze, bg="#007bff", fg="white", width=20).pack(pady=10)

lbl_result = tk.Label(root, text="", bg="#f8f8f8", wraplength=400, justify="left", fg="#333")
lbl_result.pack(pady=5)

tk.Label(root, text="Wordlist Generator", font=("Arial", 11, "bold"), bg="#f8f8f8").pack(pady=(20, 5))

frame = tk.Frame(root, bg="#f8f8f8")
frame.pack()

fields = [
    ("👤 Name", "entry_name"),
    ("🎂 DOB (ddmmyyyy)", "entry_dob"),
    ("🐾 Pet Name", "entry_pet"),
    ("📞 Phone", "entry_phone"),
    ("🌟 Idol's Name", "entry_idol"),
    ("👪 Parent's Name", "entry_parent"),
    ("👶 Child's Name", "entry_children"),
    ("💍 Spouse Name", "entry_spouse"),
    ("🏠 Hometown", "entry_hometown")
]

entry_fields = {}

for i, (label, key) in enumerate(fields):
    tk.Label(frame, text=label + ":", bg="#f8f8f8").grid(row=i, column=0, sticky="e", padx=5)
    entry = tk.Entry(frame, width=25)
    entry.grid(row=i, column=1, pady=3)
    entry_fields[key] = entry

tk.Button(root, text="Generate & Save Wordlist", command=on_generate_wordlist, bg="#28a745", fg="white", width=25).pack(pady=20)

root.mainloop()
