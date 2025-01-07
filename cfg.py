import nltk
from nltk import CFG
from nltk.parse import ChartParser
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font

# Definisi tata bahasa Bali dalam format CFG
grammar = """
    K -> S P | S P Pel | S P Ket | S P Pel Ket
    S -> NP
    P -> NP
    Pel -> NP | AdjP
    Ket -> PP
    NP -> Pronoun | Pronoun Det | Noun | Noun Det | Noun Noun | Noun Pronoun
    AdjP -> Adv Adj | Adj
    PP -> Prep NP

    Pronoun -> 'Ia' | 'Tiang'
    Noun -> 'Bapak' | 'Bale' | 'Pekak' | 'Dadong' | 'Anak' | 'Ibu' | 'Beli' | 'Pejabat' | 'Umah' | 'Dagang' | 'Nasi'  | 'Mahasiswa' | 'Mangku' | 'Penyanyi' | 'Anggota' | 'DPRD' | 'Guru' | 'Matematika' | 'Kelas' | '12' | 'SMA' | 'Ketua' | 'Panitia' | 'Jurusan' | 'Kedokteran' | 'Lomba' | 'Busana' | 'Badung' | 'Mengwi' | 'Peken' | 'Cabang' | 'Daerah' | 'Udayana' | 'Pidan' | 'Desane' | 'Putri' | 'Kampus'
    Det -> 'Ento' | 'Punika' | 'Puniki'
    Adv -> 'Paling'
    Adj -> 'Jegeg'
    Prep -> 'Di' | 'Ring' | 'Uli'
"""

def custom_tokenize(sentence):
    """Tokenisasi sederhana menggunakan metode split."""
    return sentence.split()

def parse_sentence(sentence):
    """Memproses kalimat dan menentukan hasil parsing serta kategori kata."""
    try:
        # Buat parser dari tata bahasa
        grammar_def = CFG.fromstring(grammar)
        parser = ChartParser(grammar_def)
        
        # Tokenisasi kalimat menggunakan metode custom
        tokens = custom_tokenize(sentence)
        print("Tokens:", tokens)
        
        # Parsing kalimat
        trees = list(parser.parse(tokens))
        if trees:
            print("\nHasil parsing:")
            max_trees = 10  # Set a limit for the number of trees to display
            for i, tree in enumerate(trees[:max_trees]):
                print(tree)
                tree.pretty_print()
                check_nominal_predicate(tree)
            print("\nKategori kata:")
            for token in tokens:
                find_category(token, grammar_def)
        else:
            print("\nKalimat tidak sesuai dengan aturan tata bahasa.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Pastikan tata bahasa dan masukan kalimat sesuai.")

def find_category(token, grammar_def):
    """Menentukan kategori sebuah kata berdasarkan aturan tata bahasa."""
    for production in grammar_def.productions():
        if token in production.rhs():
            print(f"'{token}' termasuk dalam kategori: {production.lhs()}")
            return
    print(f"'{token}' tidak ditemukan dalam aturan tata bahasa.")

def check_nominal_predicate(tree):
    """Memeriksa apakah predikat (P) adalah NP dan menampilkan informasi tambahan."""
    for subtree in tree.subtrees():
        if subtree.label() == 'P':  # Jika label adalah P
            if 'NP' in [child.label() for child in subtree]:  # Jika P berisi NP
                print("\nKalimat ini termasuk kalimat berpredikat nomina.")
                return
    print("\nKalimat ini tidak termasuk kalimat berpredikat nomina.")

def on_parse():
    sentence = input_text.get("1.0", tk.END).strip()
    if sentence:
        output_text.delete("1.0", tk.END)
        try:
            grammar_def = CFG.fromstring(grammar)
            parser = ChartParser(grammar_def)
            tokens = custom_tokenize(sentence)
            output_text.insert(tk.END, f"Tokens: {tokens}\n")
            trees = list(parser.parse(tokens))
            
            if trees:
                # Gunakan set untuk menyimpan hasil parsing yang unik
                parsed_trees = set()
                output_text.insert(tk.END, "\nHasil parsing:\n")
                
                for tree in trees:
                    tree_str = tree.pformat()  # Konversi tree ke format string
                    if tree_str not in parsed_trees:
                        parsed_trees.add(tree_str)  # Tambahkan tree ke dalam set unik
                        output_text.insert(tk.END, f"{tree}\n")
                        output_text.insert(tk.END, tree.pformat() + "\n")
                        gui_check_nominal_predicate(tree)
                
                for token in tokens:
                    gui_find_category(token, grammar_def)
            else:
                output_text.insert(tk.END, "\nKalimat tidak sesuai dengan aturan tata bahasa.\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error: {str(e)}\nPastikan tata bahasa dan masukan kalimat sesuai.\n")


def gui_find_category(token, grammar_def):
    for production in grammar_def.productions():
        if token in production.rhs():
            output_text.insert(tk.END, f"'{token}' termasuk dalam kategori: {production.lhs()}\n")
            return
    output_text.insert(tk.END, f"'{token}' tidak ditemukan dalam aturan tata bahasa.\n")

def gui_check_nominal_predicate(tree):
    for subtree in tree.subtrees():
        if subtree.label() == 'P':
            if 'NP' in [child.label() for child in subtree]:
                output_text.insert(tk.END, "\nKalimat ini termasuk kalimat berpredikat nomina.\n")
                return
    output_text.insert(tk.END, "\nKalimat ini tidak termasuk kalimat berpredikat nomina.\n")

# GUI setup
root = tk.Tk()
root.title("Parser Kalimat Bahasa Bali Berpredikat Nomina")
root.configure(bg="#e0f7fa")

# Set default font
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=10)

frame = tk.Frame(root, padx=10, pady=10, bg="#e0f7fa")
frame.pack(fill=tk.BOTH, expand=True)

input_label = tk.Label(frame, text="Masukkan kalimat dalam Bahasa Bali:", font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#00796b")
input_label.pack(anchor="w", pady=(0, 5))

input_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=5, font=("Helvetica", 10), bg="#ffffff", fg="#000000", borderwidth=2, relief="groove")
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

parse_button = tk.Button(frame, text="Parse", command=on_parse, font=("Helvetica", 10, "bold"), bg="#00796b", fg="white", borderwidth=2, relief="raised")
parse_button.pack(pady=10)

output_label = tk.Label(frame, text="Output:", font=("Helvetica", 12, "bold"), bg="#e0f7fa", fg="#00796b")
output_label.pack(anchor="w", pady=(10, 5))

output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=15, font=("Helvetica", 10), bg="#ffffff", fg="#000000", borderwidth=2, relief="groove")
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
# Additional GUI customization
root.geometry("800x600")  # Set window size

# Customize the input text box
input_text.configure(font=("Courier New", 12), bg="#f0f4c3", fg="#1b5e20")

# Customize the output text box
output_text.configure(font=("Courier New", 12), bg="#e8f5e9", fg="#1b5e20")

# Add a title label
title_label = tk.Label(root, text="Bali Sentence Parser", font=("Helvetica", 16, "bold"), bg="#004d40", fg="white")
title_label.pack(pady=10)

# Add padding to the frame
frame.configure(padx=20, pady=20)

# Customize the parse button
parse_button.configure(font=("Helvetica", 12, "bold"), bg="#004d40", fg="white", activebackground="#00796b", activeforeground="white")

# Run the main loop
root.mainloop()