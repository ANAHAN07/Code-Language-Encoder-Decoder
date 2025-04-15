import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import base64


# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.',  'F': '..-.', 'G': '--.',  'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--', 'N': '-.',   'O': '---',  'P': '.--.',
    'Q': '--.-','R': '.-.', 'S': '...',  'T': '-',
    'U': '..-','V': '...-', 'W': '.--',  'X': '-..-',
    'Y': '-.--','Z': '--..',
    '1': '.----','2': '..---','3': '...--','4': '....-','5': '.....',
    '6': '-....','7': '--...','8': '---..','9': '----.','0': '-----',
    ' ': '/'
}
INVERSE_MORSE = {v: k for k, v in MORSE_CODE_DICT.items()}


# Fun Code Mapping
FUN_DICT = {'a': '@', 'e': '3', 'i': '!', 'o': '0', 'u': 'µ'}
REVERSE_FUN_DICT = {v: k for k, v in FUN_DICT.items()}


# Caesar Cipher
def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift_val = shift if mode == "Encode" else -shift
            result += chr((ord(char) - base + shift_val) % 26 + base)
        else:
            result += char
    return result


# Morse Code
def morse_code(text, mode):
    if mode == "Encode":
        return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)
    else:
        return ''.join(INVERSE_MORSE.get(code, '') for code in text.split())


# Base64
def base64_code(text, mode):
    if mode == "Encode":
        return base64.b64encode(text.encode()).decode()
    else:
        try:
            return base64.b64decode(text.encode()).decode()
        except Exception:
            return "Invalid Base64!"


# Fun Code
def fun_code(text, mode):
    if mode == "Encode":
        return ''.join(FUN_DICT.get(char.lower(), char) for char in text)
    else:
        return ''.join(REVERSE_FUN_DICT.get(char, char) for char in text)


# Process Text
def process_text():
    text = entry_text.get()
    code_type = dropdown_code.get()
    mode = dropdown_mode.get()

    if not text or not code_type or not mode:
        messagebox.showerror("Missing Input", "Please fill all fields.")
        return

    try:
        if code_type == "Caesar Cipher":
            shift = int(entry_shift.get())
            result = caesar_cipher(text, shift, mode)
        elif code_type == "Morse Code":
            result = morse_code(text, mode)
        elif code_type == "Base64":
            result = base64_code(text, mode)
        elif code_type == "Fun Language":
            result = fun_code(text, mode)
        else:
            result = "Invalid Code Type!"
    except Exception as e:
        result = f"Error: {e}"

    output_text.set(result)


# Save to File
def save_to_file():
    result = output_text.get()
    original = entry_text.get()
    method = dropdown_code.get()
    mode = dropdown_mode.get()

    if not result:
        messagebox.showwarning("No Result", "Please encode or decode something first.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if file_path:
        try:
            with open(file_path, "w") as f:
                f.write(f"Original Text: {original}\n")
                f.write(f"Method: {method}\n")
                f.write(f"Mode: {mode}\n")
                f.write(f"Result: {result}\n")
            messagebox.showinfo("Success", f"Saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Setupping GUI 
root = tk.Tk()
root.title("Code Language Encoder & Decoder 🧠🔐")
root.geometry("500x430")
root.config(padx=20, pady=20, bg="#2e3b4e")


# Disable resizing
root.resizable(False, False)


# Label Styling
label_font = ('Helvetica', 12)
label_fg = '#ffffff'
label_bg = '#2e3b4e'


# Button Styling
button_fg = '#ffffff'
button_bg = '#4CAF50'  # Green Button


tk.Label(root, text="Enter Text:", font=label_font, fg=label_fg, bg=label_bg).pack()
entry_text = tk.Entry(root, width=50, bg='#f2f2f2', fg='#000000', font=('Helvetica', 12))
entry_text.pack()


tk.Label(root, text="Choose Code Type:", font=label_font, fg=label_fg, bg=label_bg).pack()
dropdown_code = ttk.Combobox(root, values=["Caesar Cipher", "Morse Code", "Base64", "Fun Language"], font=('Helvetica', 12))
dropdown_code.pack()


tk.Label(root, text="Choose Mode:", font=label_font, fg=label_fg, bg=label_bg).pack()
dropdown_mode = ttk.Combobox(root, values=["Encode", "Decode"], font=('Helvetica', 12))
dropdown_mode.pack()


tk.Label(root, text="Shift (Caesar Only):", font=label_font, fg=label_fg, bg=label_bg).pack()
entry_shift = tk.Entry(root, width=10, bg='#f2f2f2', fg='#000000', font=('Helvetica', 12))
entry_shift.pack()


tk.Button(root, text="Process", command=process_text, fg=button_fg, bg=button_bg, font=('Helvetica', 12)).pack(pady=10)
tk.Button(root, text="Save Result to File 💾", command=save_to_file, fg=button_fg, bg=button_bg, font=('Helvetica', 12)).pack(pady=5)


tk.Label(root, text="Result:", font=label_font, fg=label_fg, bg=label_bg).pack()
output_text = tk.StringVar()
tk.Entry(root, textvariable=output_text, width=50, state="readonly", bg='#f2f2f2', fg='#000000', font=('Helvetica', 12)).pack()


root.mainloop()