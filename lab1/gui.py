"""
Laboratory Work No. 1 - Cryptography and Security
Simple Tkinter GUI for Task 1.1 (Caesar cipher) and
Task 1.2 (Caesar cipher with two keys) over the Romanian alphabet.

Run:  python gui.py
"""

import tkinter as tk
from tkinter import ttk, font as tkfont

from cipher import (ALPHABET, N, normalize, parse_key, parse_keyword,
                    permuted_alphabet, encrypt, decrypt)

ERROR_BG = "#FDE2E2"
OK_BG = "white"


class CaesarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 1 - Caesar Cipher (Romanian alphabet, n = 31)")
        self.resizable(False, False)
        tkfont.nametofont("TkDefaultFont").configure(size=12)
        tkfont.nametofont("TkTextFont").configure(size=12)
        self.mono = tkfont.nametofont("TkFixedFont").copy()
        self.mono.configure(size=12)
        self.bold = tkfont.nametofont("TkDefaultFont").copy()
        self.bold.configure(weight="bold")

        self.task = tk.StringVar(value="1")      # "1" = Task 1.1, "2" = Task 1.2
        self.op = tk.StringVar(value="E")        # "E" = encrypt, "D" = decrypt
        self._build()
        self._on_task_change()

    # ------------------------------------------------------------ layout
    def _build(self):
        pad = {"padx": 10, "pady": 5}
        main = ttk.Frame(self, padding=14)
        main.grid()
        form = ttk.Frame(main)
        form.grid(row=0, column=0, sticky="w")

        ttk.Label(form, text="Caesar cipher - Romanian alphabet (n = 31)",
                  font=self.bold).grid(row=0, column=0, columnspan=3, sticky="w", **pad)

        ttk.Label(form, text="Task:").grid(row=1, column=0, sticky="w", **pad)
        tasks = ttk.Frame(form)
        tasks.grid(row=1, column=1, columnspan=2, sticky="w")
        ttk.Radiobutton(tasks, text="1.1 Caesar cipher", value="1", variable=self.task,
                        command=self._on_task_change).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(tasks, text="1.2 Caesar with permutation (two keys)", value="2",
                        variable=self.task, command=self._on_task_change).pack(side="left")

        ttk.Label(form, text="Operation:").grid(row=2, column=0, sticky="w", **pad)
        ops = ttk.Frame(form)
        ops.grid(row=2, column=1, columnspan=2, sticky="w")
        ttk.Radiobutton(ops, text="Encrypt", value="E", variable=self.op,
                        command=self._on_op_change).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(ops, text="Decrypt", value="D", variable=self.op,
                        command=self._on_op_change).pack(side="left")

        ttk.Label(form, text="Key 1 (shift):").grid(row=3, column=0, sticky="w", **pad)
        self.key1 = tk.Entry(form, width=8, font=self.mono, bg=OK_BG)
        self.key1.grid(row=3, column=1, sticky="w", **pad)
        ttk.Label(form, text=f"integer from 1 to {N - 1}", foreground="gray40").grid(
            row=3, column=2, sticky="w")

        self.key2_label = ttk.Label(form, text="Key 2 (keyword):")
        self.key2_label.grid(row=4, column=0, sticky="w", **pad)
        self.key2 = tk.Entry(form, width=30, font=self.mono, bg=OK_BG)
        self.key2.grid(row=4, column=1, sticky="w", **pad)
        self.key2_hint = ttk.Label(form, text="Romanian letters only, at least 7",
                                   foreground="gray40")
        self.key2_hint.grid(row=4, column=2, sticky="w")

        self.text_label = ttk.Label(form, text="Message:")
        self.text_label.grid(row=5, column=0, sticky="w", **pad)
        self.text = tk.Entry(form, width=52, font=self.mono, bg=OK_BG)
        self.text.grid(row=5, column=1, columnspan=2, sticky="w", **pad)

        btns = ttk.Frame(form)
        btns.grid(row=6, column=1, columnspan=2, sticky="w", **pad)
        self.run_btn = ttk.Button(btns, text="Encrypt", command=self.run)
        self.run_btn.pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left")

        ttk.Label(form, text="Normalized:").grid(row=7, column=0, sticky="w", **pad)
        self.norm_out = tk.Entry(form, width=52, font=self.mono, state="readonly")
        self.norm_out.grid(row=7, column=1, columnspan=2, sticky="w", **pad)

        self.result_label = ttk.Label(form, text="Ciphertext:", font=self.bold)
        self.result_label.grid(row=8, column=0, sticky="w", **pad)
        self.result = tk.Entry(form, width=52, font=self.mono, state="readonly",
                               readonlybackground="#E8F5E9")
        self.result.grid(row=8, column=1, columnspan=2, sticky="w", **pad)

        self.status = ttk.Label(main, text=" ", foreground="#C62828", wraplength=1100)
        self.status.grid(row=1, column=0, sticky="w", **pad)

        self.alpha_title = ttk.Label(main, text="Alphabet used:", font=self.bold)
        self.alpha_title.grid(row=2, column=0, sticky="w", padx=10, pady=(8, 2))
        grid = ttk.Frame(main)
        grid.grid(row=3, column=0, sticky="w", padx=10, pady=(0, 6))
        tk.Label(grid, text="Code", font=self.bold, width=6, anchor="w").grid(row=0, column=0)
        tk.Label(grid, text="Letter", font=self.bold, width=6, anchor="w").grid(row=1, column=0)
        self.cells = []
        for i in range(N):
            tk.Label(grid, text=str(i), width=3, relief="solid", bd=1,
                     bg="#E3EAF5").grid(row=0, column=i + 1)
            cell = tk.Label(grid, text="", width=3, relief="solid", bd=1,
                            bg="white", font=self.mono)
            cell.grid(row=1, column=i + 1)
            self.cells.append(cell)
        self.show_alphabet(ALPHABET)

        self.bind("<Return>", lambda e: self.run())

    # ------------------------------------------------------------ helpers
    def show_alphabet(self, alphabet):
        for cell, letter in zip(self.cells, alphabet):
            cell.config(text=letter)

    def _set_readonly(self, entry, value):
        entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.config(state="readonly")

    def _on_task_change(self):
        two_keys = self.task.get() == "2"
        self.key2.config(state="normal" if two_keys else "disabled", bg=OK_BG)
        self.alpha_title.config(text="Permuted alphabet (Key 2):" if two_keys
                                else "Alphabet used (Table 2):")
        self.show_alphabet(ALPHABET)
        self._clear_outputs()

    def _on_op_change(self):
        enc = self.op.get() == "E"
        self.run_btn.config(text="Encrypt" if enc else "Decrypt")
        self.text_label.config(text="Message:" if enc else "Ciphertext:")
        self.result_label.config(text="Ciphertext:" if enc else "Decrypted:")
        self._clear_outputs()

    def _clear_outputs(self):
        self._set_readonly(self.norm_out, "")
        self._set_readonly(self.result, "")
        self.status.config(text=" ")

    def clear(self):
        for e in (self.key1, self.key2, self.text):
            st = e.cget("state")
            e.config(state="normal", bg=OK_BG)
            e.delete(0, "end")
            e.config(state=st)
        self._on_task_change()

    def _error(self, entry, message):
        """Show the message, mark the field and ask for the value again."""
        entry.config(bg=ERROR_BG)
        entry.focus_set()
        entry.select_range(0, "end")
        self.status.config(text="Error: " + str(message))
        self._set_readonly(self.result, "")
        self._set_readonly(self.norm_out, "")

    # ------------------------------------------------------------ action
    def run(self):
        for e in (self.key1, self.key2, self.text):
            if e.cget("state") == "normal":
                e.config(bg=OK_BG)
        try:
            k = parse_key(self.key1.get())
        except ValueError as err:
            return self._error(self.key1, err)

        alphabet = ALPHABET
        if self.task.get() == "2":
            try:
                keyword = parse_keyword(self.key2.get())
            except ValueError as err:
                return self._error(self.key2, err)
            alphabet = permuted_alphabet(keyword)
        self.show_alphabet(alphabet)

        try:
            text = normalize(self.text.get())
        except ValueError as err:
            return self._error(self.text, err)

        out = encrypt(text, k, alphabet) if self.op.get() == "E" else decrypt(text, k, alphabet)
        self._set_readonly(self.norm_out, text)
        self._set_readonly(self.result, out)
        self.status.config(text=" ")


if __name__ == "__main__":
    CaesarApp().mainloop()
