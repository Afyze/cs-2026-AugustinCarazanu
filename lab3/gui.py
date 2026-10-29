"""
Laboratory Work No. 3 - Cryptography and Security
Simple Tkinter GUI for the Playfair cipher in Romanian (Task 3.1).

Run:  python gui.py
"""

import tkinter as tk
from tkinter import ttk, font as tkfont

from playfair import ROWS, COLS, encrypt, decrypt, build_matrix, parse_key

ERROR_BG = "#FDE2E2"
OK_BG = "white"


class PlayfairApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 3 - Playfair cipher (Romanian alphabet)")
        self.resizable(False, False)
        tkfont.nametofont("TkDefaultFont").configure(size=12)
        self.mono = tkfont.Font(family="Courier", size=13)
        self.cell_font = tkfont.Font(family="Courier", size=16, weight="bold")
        self.bold = tkfont.nametofont("TkDefaultFont").copy()
        self.bold.configure(weight="bold")
        self.op = tk.StringVar(value="E")
        self._build()
        self.show_matrix(None)

    # ------------------------------------------------------------ layout
    def _build(self):
        pad = {"padx": 8, "pady": 5}
        main = ttk.Frame(self, padding=14)
        main.grid()
        form = ttk.Frame(main)
        form.grid(row=0, column=0, sticky="nw")
        side = ttk.Frame(main)
        side.grid(row=0, column=1, sticky="nw", padx=(24, 0))

        ttk.Label(form, text="Playfair cipher - Romanian alphabet (5 x 6 matrix, J = I)",
                  font=self.bold).grid(row=0, column=0, columnspan=2, sticky="w", **pad)

        ttk.Label(form, text="Operation:").grid(row=1, column=0, sticky="w", **pad)
        ops = ttk.Frame(form)
        ops.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(ops, text="Encrypt", value="E", variable=self.op,
                        command=self._on_op).pack(side="left", padx=(0, 16))
        ttk.Radiobutton(ops, text="Decrypt", value="D", variable=self.op,
                        command=self._on_op).pack(side="left")

        ttk.Label(form, text="Key:").grid(row=2, column=0, sticky="w", **pad)
        self.key = tk.Entry(form, width=40, font=self.mono, bg=OK_BG)
        self.key.grid(row=2, column=1, sticky="w", **pad)
        self.key.bind("<KeyRelease>", lambda e: self.preview_matrix())
        ttk.Label(form, text="at least 7 letters", foreground="gray40").grid(
            row=3, column=1, sticky="w", padx=8)

        self.text_label = ttk.Label(form, text="Message:")
        self.text_label.grid(row=4, column=0, sticky="nw", **pad)
        self.text = tk.Text(form, width=40, height=4, font=self.mono, wrap="word", bg=OK_BG)
        self.text.grid(row=4, column=1, sticky="w", **pad)

        btns = ttk.Frame(form)
        btns.grid(row=5, column=1, sticky="w", **pad)
        self.run_btn = ttk.Button(btns, text="Encrypt", command=self.run)
        self.run_btn.pack(side="left", padx=(0, 8))
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left")

        ttk.Label(form, text="Pairs:").grid(row=6, column=0, sticky="nw", **pad)
        self.pairs = tk.Text(form, width=40, height=3, font=self.mono, wrap="word",
                             state="disabled", bg="#F2F2F2")
        self.pairs.grid(row=6, column=1, sticky="w", **pad)

        self.result_label = ttk.Label(form, text="Cryptogram:", font=self.bold)
        self.result_label.grid(row=7, column=0, sticky="nw", **pad)
        self.result = tk.Text(form, width=40, height=3, font=self.mono, wrap="word",
                              state="disabled", bg="#E8F5E9")
        self.result.grid(row=7, column=1, sticky="w", **pad)

        self.status = ttk.Label(form, text=" ", foreground="#C62828", wraplength=520)
        self.status.grid(row=8, column=0, columnspan=2, sticky="w", **pad)

        ttk.Label(side, text="Encryption matrix", font=self.bold).grid(row=0, column=0, sticky="w")
        grid = ttk.Frame(side)
        grid.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.cells = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                lbl = tk.Label(grid, text="", width=3, height=1, font=self.cell_font,
                               relief="solid", bd=1, bg="white")
                lbl.grid(row=r, column=c, padx=1, pady=1)
                row.append(lbl)
            self.cells.append(row)
        ttk.Label(side, text="Blue: letters of the key", foreground="gray40").grid(
            row=2, column=0, sticky="w", pady=(6, 0))

    # ------------------------------------------------------------ helpers
    def _set(self, widget, value):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.config(state="disabled")

    def show_matrix(self, matrix, key_len=0):
        for r in range(ROWS):
            for c in range(COLS):
                ch = matrix[r][c] if matrix else ""
                in_key = r * COLS + c < key_len
                self.cells[r][c].config(text=ch, bg="#DCE6F8" if in_key else "white")

    def preview_matrix(self):
        try:
            key = parse_key(self.key.get())
        except ValueError:
            self.show_matrix(None)
            return
        self.show_matrix(build_matrix(key), len(dict.fromkeys(key)))

    def _on_op(self):
        enc = self.op.get() == "E"
        self.run_btn.config(text="Encrypt" if enc else "Decrypt")
        self.text_label.config(text="Message:" if enc else "Cryptogram:")
        self.result_label.config(text="Cryptogram:" if enc else "Decrypted text:")
        self._clear_out()

    def _clear_out(self):
        self._set(self.pairs, "")
        self._set(self.result, "")
        self.status.config(text=" ")

    def clear(self):
        self.key.delete(0, "end")
        self.text.delete("1.0", "end")
        self.key.config(bg=OK_BG)
        self.text.config(bg=OK_BG)
        self.show_matrix(None)
        self._clear_out()

    def _error(self, widget, message):
        widget.config(bg=ERROR_BG)
        widget.focus_set()
        self.status.config(text="Error: " + str(message), foreground="#C62828")
        self._set(self.pairs, "")
        self._set(self.result, "")

    # ------------------------------------------------------------ action
    def run(self):
        self.key.config(bg=OK_BG)
        self.text.config(bg=OK_BG)
        try:
            key = parse_key(self.key.get())
        except ValueError as err:
            self.show_matrix(None)
            return self._error(self.key, err)
        self.show_matrix(build_matrix(key), len(dict.fromkeys(key)))
        func = encrypt if self.op.get() == "E" else decrypt
        try:
            _, pairs, out = func(self.text.get("1.0", "end"), self.key.get())
        except ValueError as err:
            return self._error(self.text, err)
        self._set(self.pairs, " ".join(pairs))
        result = " ".join(out) if self.op.get() == "E" else "".join(out)
        self._set(self.result, result)
        self.status.config(text=" " if self.op.get() == "E" else
                           "Add the spaces and remove the filler letters (X / Q) manually.",
                           foreground="gray30")


if __name__ == "__main__":
    PlayfairApp().mainloop()
