# Cryptography and Security – Laboratory Works

**Student:** Augustin Carazanu, FAF-243  
**Teacher:** assist. univ. Maia Zaica  
Technical University of Moldova, FCIM

| Lab | Topic | Folder |
|-----|-------|--------|
| 1 | The Caesar Cipher and the Caesar Cipher with a Permutation | [lab1](lab1) |
| 2 | Cryptanalysis of Monoalphabetic Ciphers (frequency analysis, variant 3) | [lab2](lab2) |

## Lab 1 – Caesar cipher (Romanian alphabet, n = 31)

- **Task 1.1** – Caesar cipher with a numeric key from 1 to 30.
- **Task 1.2** – Caesar cipher with two keys: a numeric shift and a keyword (at least 7 Romanian letters) that permutes the alphabet.

Letters are encoded as `A = 0, Ă = 1, …, Z = 30`; character codes (ASCII/Unicode) are not used for the shift. Text is converted to uppercase and spaces are removed. Ş/Ţ typed with a cedilla are accepted as Ș/Ț.

### Run

Requires Python 3 with Tkinter (included in the standard installers).

```bash
cd lab1
python3 gui.py
```

### Files

- `lab1/cipher.py` – letter encoding, validation, permuted alphabet, encryption and decryption
- `lab1/gui.py` – Tkinter interface
- `lab1/screenshots/` – screenshots used in the report
- `lab1/Lab1_AugustinCarazanu_FAF-243.docx` – the report

## Lab 2 – Cryptanalysis of monoalphabetic ciphers (variant 3)

The intercepted English ciphertext is broken by frequency analysis. The Tkinter tool counts the letter
frequencies, compares them with English, shows the most frequent digrams and trigrams and applies a
partial key after every guess (solved letters in lowercase, unknown ones in UPPERCASE).

```bash
cd lab2
python3 gui.py
```

- `lab2/analysis.py` – frequencies, n-grams, partial key, key check
- `lab2/gui.py` – Tkinter interface
- `lab2/ciphertext_v3.txt` – the ciphertext of variant 3
- `lab2/screenshots/` – screenshots used in the report
- `lab2/Lab2_AugustinCarazanu_FAF-243.docx` – the report
