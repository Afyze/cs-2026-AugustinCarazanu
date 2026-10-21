"""
Laboratory Work No. 2 - Cryptography and Security
Tkinter tool for breaking a monoalphabetic cipher by frequency analysis.

Run:  python gui.py            (loads ciphertext_v3.txt)
"""

import os
import tkinter as tk
from tkinter import ttk, font as tkfont

from analysis import (ALPHABET, ENGLISH_FREQ, ENGLISH_ORDER, frequencies, sorted_by_frequency,
                      ngrams, frequency_guess, apply_key, decrypt, check_key)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(HERE, "ciphertext_v3.txt")
CIPHER_COLOR = "#2F6DB5"
ENGLISH_COLOR = "#B8B8B8"


class FrequencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 2 - Frequency analysis of a monoalphabetic cipher")
        tkfont.nametofont("TkDefaultFont").configure(size=11)
        self.mono = tkfont.Font(family="Courier", size=11)
        self.bold = tkfont.nametofont("TkDefaultFont").copy()
        self.bold.configure(weight="bold")
        self.key_vars = {}
        self._build()
        self.load_default()

    # ------------------------------------------------------------ layout
    def _build(self):
        main = ttk.Frame(self, padding=10)
        main.grid(sticky="nsew")

        left = ttk.Frame(main)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(left, text="Ciphertext", font=self.bold).grid(row=0, column=0, sticky="w")
        self.cipher = tk.Text(left, width=78, height=12, wrap="word", font=self.mono)
        self.cipher.grid(row=1, column=0, sticky="nsew")

        btns = ttk.Frame(left)
        btns.grid(row=2, column=0, sticky="w", pady=6)
        ttk.Button(btns, text="Analyze", command=self.analyze).pack(side="left", padx=(0, 6))
        ttk.Button(btns, text="Guess key by frequency", command=self.guess).pack(side="left", padx=(0, 6))
        ttk.Button(btns, text="Clear key", command=self.clear_key).pack(side="left")

        ttk.Label(left, text="Key (cipher letter -> plain letter)", font=self.bold).grid(
            row=3, column=0, sticky="w", pady=(4, 2))
        keyf = ttk.Frame(left)
        keyf.grid(row=4, column=0, sticky="w")
        for i, ch in enumerate(ALPHABET):
            r, c = divmod(i, 13)
            tk.Label(keyf, text=ch, font=self.bold, width=3).grid(row=2 * r, column=c)
            var = tk.StringVar()
            var.trace_add("write", lambda *_: self.update_output())
            e = tk.Entry(keyf, textvariable=var, width=3, justify="center", font=self.mono)
            e.grid(row=2 * r + 1, column=c, padx=1, pady=(0, 4))
            self.key_vars[ch] = var

        self.status = ttk.Label(left, text=" ", foreground="#C62828")
        self.status.grid(row=5, column=0, sticky="w")

        ttk.Label(left, text="Result (solved letters in lowercase, unknown ones in UPPERCASE)",
                  font=self.bold).grid(row=6, column=0, sticky="w", pady=(4, 2))
        self.output = tk.Text(left, width=78, height=12, wrap="word", font=self.mono, bg="#F7FAF7")
        self.output.grid(row=7, column=0, sticky="nsew")
        self.output.tag_configure("solved", foreground="#1B7F3B")
        self.output.tag_configure("unknown", foreground="#9A2A2A")

        ttk.Label(right, text="Letter frequencies (%)", font=self.bold).grid(row=0, column=0, sticky="w")
        self.chart = tk.Canvas(right, width=560, height=250, bg="white", highlightthickness=1,
                               highlightbackground="#CCCCCC")
        self.chart.grid(row=1, column=0, sticky="w")

        cols = ("rank", "cipher", "count", "pct", "eng", "engpct")
        self.table = ttk.Treeview(right, columns=cols, show="headings", height=13)
        for col, title, w in zip(cols, ("#", "Cipher", "Count", "%", "English", "%"),
                                 (36, 70, 70, 70, 80, 70)):
            self.table.heading(col, text=title)
            self.table.column(col, width=w, anchor="center")
        self.table.grid(row=2, column=0, sticky="w", pady=(8, 4))

        ttk.Label(right, text="Most frequent digrams / trigrams", font=self.bold).grid(
            row=3, column=0, sticky="w")
        self.grams = ttk.Label(right, text="", font=self.mono, justify="left")
        self.grams.grid(row=4, column=0, sticky="w")

    # ------------------------------------------------------------ actions
    def load_default(self):
        if os.path.exists(DEFAULT_FILE):
            with open(DEFAULT_FILE, encoding="utf8") as f:
                self.cipher.insert("1.0", f.read().strip())
        self.analyze()

    def text(self):
        return self.cipher.get("1.0", "end").strip()

    def key(self):
        return {ch: v.get().strip().upper() for ch, v in self.key_vars.items() if v.get().strip()}

    def analyze(self):
        freq = frequencies(self.text())
        order = sorted_by_frequency(freq)
        self.table.delete(*self.table.get_children())
        for i, ch in enumerate(order):
            eng = ENGLISH_ORDER[i]
            self.table.insert("", "end", values=(i + 1, ch, freq[ch][0], f"{freq[ch][1]:.2f}",
                                                 eng, f"{ENGLISH_FREQ[eng]:.2f}"))
        self.draw_chart(freq)
        bi = "  ".join(f"{g}:{n}" for g, n in ngrams(self.text(), 2, 8))
        tri = "  ".join(f"{g}:{n}" for g, n in ngrams(self.text(), 3, 7))
        self.grams.config(text=bi + "\n" + tri)
        self.update_output()

    def draw_chart(self, freq):
        c = self.chart
        c.delete("all")
        w, h, left, bottom, top = 560, 250, 30, 30, 12
        peak = max(max(p for _, p in freq.values()), max(ENGLISH_FREQ.values()))
        slot = (w - left - 8) / 26
        for i, ch in enumerate(ALPHABET):
            x = left + i * slot
            for j, (val, color) in enumerate(((ENGLISH_FREQ[ch], ENGLISH_COLOR), (freq[ch][1], CIPHER_COLOR))):
                bh = (h - bottom - top) * val / peak
                x0 = x + 2 + j * (slot - 4) / 2
                c.create_rectangle(x0, h - bottom - bh, x0 + (slot - 4) / 2, h - bottom, fill=color, width=0)
            c.create_text(x + slot / 2, h - bottom + 10, text=ch, font=("Courier", 9))
        c.create_line(left, h - bottom, w - 4, h - bottom)
        c.create_rectangle(left + 8, 8, left + 20, 18, fill=CIPHER_COLOR, width=0)
        c.create_text(left + 24, 13, text="ciphertext", anchor="w", font=("TkDefaultFont", 9))
        c.create_rectangle(left + 110, 8, left + 122, 18, fill=ENGLISH_COLOR, width=0)
        c.create_text(left + 126, 13, text="English (Table 2.2)", anchor="w", font=("TkDefaultFont", 9))

    def guess(self):
        for c, p in frequency_guess(frequencies(self.text())).items():
            self.key_vars[c].set(p)

    def clear_key(self):
        for v in self.key_vars.values():
            v.set("")

    def set_key(self, key):
        self.clear_key()
        for c, p in key.items():
            self.key_vars[c].set(p)

    def update_output(self):
        key = self.key()
        err = check_key(key)
        self.status.config(text=("Error: " + err) if err else
                           f"{len(key)} of 26 letters in the key.")
        self.status.config(foreground="#C62828" if err else "gray30")
        result = apply_key(self.text(), key)
        self.output.delete("1.0", "end")
        for ch in result:
            tag = "solved" if ch.islower() else ("unknown" if ch.isupper() else "")
            self.output.insert("end", ch, tag)
        if len(key) == 26 and not err:
            self.output.delete("1.0", "end")
            self.output.insert("1.0", decrypt(self.text(), key), "solved")


if __name__ == "__main__":
    FrequencyApp().mainloop()
