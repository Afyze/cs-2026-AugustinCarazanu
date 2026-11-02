"""
Laboratory Work No. 4 - Cryptography and Security
Tkinter GUI for Task 2.3: given K+, determine the DES round key Ki.
All the tables used and every intermediate step are displayed.

Run:  python gui.py
"""

import tkinter as tk
from tkinter import ttk, font as tkfont

from des_keys import (PC1, PC2, SHIFTS, parse_kplus, parse_round, random_kplus,
                      kplus_from_key, round_key, group, to_hex)

ERROR_BG = "#FDE2E2"
OK_BG = "white"


def table_text(table, cols):
    rows = [table[i:i + cols] for i in range(0, len(table), cols)]
    return "\n".join("   " + " ".join(f"{v:>3}" for v in r) for r in rows)


class KeyScheduleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 4 - DES round key Ki from K+ (Task 2.3)")
        tkfont.nametofont("TkDefaultFont").configure(size=12)
        self.mono = tkfont.Font(family="Courier", size=12)
        self.bold = tkfont.nametofont("TkDefaultFont").copy()
        self.bold.configure(weight="bold")
        self._build()

    # ------------------------------------------------------------ layout
    def _build(self):
        pad = {"padx": 8, "pady": 4}
        main = ttk.Frame(self, padding=12)
        main.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        form = ttk.Frame(main)
        form.grid(row=0, column=0, sticky="ew")

        ttk.Label(form, text="DES key schedule: K+  →  Ki", font=self.bold).grid(
            row=0, column=0, columnspan=4, sticky="w", **pad)

        ttk.Label(form, text="K+ (56 bits or 14 hex):").grid(row=1, column=0, sticky="w", **pad)
        self.kplus = tk.Entry(form, width=72, font=self.mono, bg=OK_BG)
        self.kplus.grid(row=1, column=1, columnspan=2, sticky="w", **pad)
        ttk.Button(form, text="Random K+", command=self.generate).grid(row=1, column=3, sticky="w", **pad)

        ttk.Label(form, text="or from an 8-char key:").grid(row=2, column=0, sticky="w", **pad)
        self.key8 = tk.Entry(form, width=14, font=self.mono, bg=OK_BG)
        self.key8.grid(row=2, column=1, sticky="w", **pad)
        ttk.Button(form, text="Compute K+ with PC-1", command=self.from_key).grid(
            row=2, column=2, sticky="w", **pad)

        ttk.Label(form, text="Round i (1–16):").grid(row=3, column=0, sticky="w", **pad)
        self.round = tk.Spinbox(form, from_=1, to=16, width=5, font=self.mono)
        self.round.grid(row=3, column=1, sticky="w", **pad)
        ttk.Button(form, text="Compute Ki", command=self.run).grid(row=3, column=2, sticky="w", **pad)

        self.status = ttk.Label(form, text=" ", foreground="#C62828")
        self.status.grid(row=4, column=0, columnspan=4, sticky="w", **pad)

        self.result = ttk.Label(form, text=" ", font=self.bold, foreground="#1B6E35")
        self.result.grid(row=5, column=0, columnspan=4, sticky="w", **pad)

        out = ttk.Frame(main)
        out.grid(row=1, column=0, sticky="nsew")
        out.columnconfigure(0, weight=1)
        out.rowconfigure(0, weight=1)
        self.text = tk.Text(out, width=100, height=30, font=self.mono, wrap="none", bg="#FAFAFA")
        self.text.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(out, orient="vertical", command=self.text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.text.config(yscrollcommand=sb.set)
        self.text.tag_configure("h", font=self.bold, foreground="#1F3B8A")
        self.text.tag_configure("hi", background="#FFF1C2")
        self.text.tag_configure("res", font=self.bold, foreground="#1B6E35")
        self.show_tables()

    # ------------------------------------------------------------ output helpers
    def write(self, s="", tag=None):
        self.text.insert("end", s + "\n", tag)

    def show_tables(self, i=None):
        self.write("Tables used", "h")
        self.write("PC-2 (Permuted Choice 2): 56 bits of CiDi -> 48 bits of Ki")
        self.write(table_text(PC2, 6))
        self.write()
        self.write("Left shifts per round")
        self.write("   Round:  " + " ".join(f"{n:>2}" for n in range(1, 17)))
        line = "   Shifts: " + " ".join(f"{s:>2}" for s in SHIFTS)
        self.write(line)
        if i:
            self.write("   Total shifts up to round {}: {}".format(i, sum(SHIFTS[:i])))
        self.write()

    # ------------------------------------------------------------ actions
    def _error(self, widget, msg):
        if widget is not None:
            widget.config(bg=ERROR_BG)
            widget.focus_set()
        self.status.config(text="Error: " + str(msg))
        self.result.config(text=" ")

    def _ok(self):
        for w in (self.kplus, self.key8):
            w.config(bg=OK_BG)
        self.status.config(text=" ")

    def generate(self):
        self._ok()
        self.kplus.delete(0, "end")
        self.kplus.insert(0, group(random_kplus(), 7))

    def from_key(self):
        self._ok()
        try:
            k64, kp = kplus_from_key(self.key8.get())
        except ValueError as err:
            return self._error(self.key8, err)
        self.kplus.delete(0, "end")
        self.kplus.insert(0, group(kp, 7))
        self.text.delete("1.0", "end")
        self.write("K+ obtained from the key \"{}\"".format(self.key8.get()), "h")
        self.write("K (64 bits, ASCII) = " + group(k64, 8))
        self.write("PC-1 (Permuted Choice 1): 64 bits of K -> 56 bits of K+")
        self.write(table_text(PC1, 7))
        self.write("K+ = PC-1(K)      = " + group(kp, 7), "res")
        self.result.config(text=" ")
        self.write()
        self.status.config(text="K+ is ready. Choose the round i and press “Compute Ki”.",
                           foreground="gray30")

    def run(self):
        self._ok()
        try:
            kp = parse_kplus(self.kplus.get())
        except ValueError as err:
            return self._error(self.kplus, err)
        try:
            i = parse_round(self.round.get())
        except ValueError as err:
            return self._error(None, err)
        r = round_key(kp, i)

        self.text.delete("1.0", "end")
        self.write(f"Step 1. Split K+ into two halves of 28 bits", "h")
        self.write("K+ = " + group(kp, 7))
        self.write("C0 = " + group(r["C0"], 7))
        self.write("D0 = " + group(r["D0"], 7))
        self.write()
        self.write(f"Step 2. Shift C and D to the left, rounds 1..{i}", "h")
        for n, s, c, d in r["steps"][1:]:
            tag = "hi" if n == i else None
            self.write(f"Round {n:>2} ({s} shift{'s' if s > 1 else ' '}):  "
                       f"C{n:<2}= {group(c, 7)}   D{n:<2}= {group(d, 7)}", tag)
        self.write()
        self.write(f"Step 3. Join C{i} and D{i}", "h")
        self.write(f"C{i}D{i} = " + group(r["CD"], 7))
        self.write()
        self.write(f"Step 4. Apply PC-2 to C{i}D{i} (take bits 14, 17, 11, 24, 1, 5, ...)", "h")
        self.write(f"K{i} = PC-2(C{i}D{i}) = " + group(r["K"], 6), "res")
        self.write(f"K{i} (hex) = " + to_hex(r["K"]), "res")
        self.write()
        self.show_tables(i)
        self.result.config(text=f"K{i} = {group(r['K'], 6)}   (hex {to_hex(r['K'])})")
        self.status.config(text=" ")


if __name__ == "__main__":
    KeyScheduleApp().mainloop()
