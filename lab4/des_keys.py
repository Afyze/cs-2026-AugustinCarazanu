"""
Laboratory Work No. 4 - Cryptography and Security
Task 2.3 (n = 3, 3 mod 11 = 3): given K+ in the DES algorithm,
determine the round key Ki for a given i.

Only the DES key schedule is needed:
    K (64 bits) --PC-1--> K+ (56 bits) = C0 | D0
    Cn = LS_n(Cn-1), Dn = LS_n(Dn-1)        (1 or 2 left shifts)
    Kn = PC-2(Cn | Dn)                       (48 bits)
Used by gui.py.
"""

import secrets

# Permuted choice 1 (used only when K+ is obtained from an 8-character key)
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# Permuted choice 2: 56 bits of CnDn -> 48 bits of Kn
PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Number of left shifts for rounds 1..16
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# ---------------------------------------------------------------
# Input
# ---------------------------------------------------------------
def parse_kplus(text):
    """K+ given as 56 binary digits or 14 hex digits (spaces allowed)."""
    s = "".join(text.split())
    if not s:
        raise ValueError("Enter K+ (56 bits in binary or 14 hexadecimal digits).")
    if set(s) <= {"0", "1"} and len(s) != 14:
        if len(s) != 56:
            raise ValueError(f"K+ in binary must have exactly 56 bits (it has {len(s)}).")
        return s
    if all(c in "0123456789abcdefABCDEF" for c in s):
        if len(s) != 14:
            raise ValueError(f"K+ in hexadecimal must have exactly 14 digits (it has {len(s)}).")
        return bin(int(s, 16))[2:].zfill(56)
    bad = next(c for c in s if c not in "0123456789abcdefABCDEF")
    raise ValueError(f"Invalid character '{bad}'. K+ may contain only 0/1 (56 bits) "
                     f"or hexadecimal digits 0-9, A-F (14 digits).")


def parse_round(value):
    v = str(value).strip()
    if not v.isdigit() or not 1 <= int(v) <= 16:
        raise ValueError(f"Invalid round '{v}'. i must be an integer from 1 to 16.")
    return int(v)


def random_kplus():
    return "".join(secrets.choice("01") for _ in range(56))


def key_to_bits(key):
    """8 ASCII characters -> 64 bits."""
    if len(key) != 8:
        raise ValueError(f"The key must have exactly 8 characters (it has {len(key)}).")
    if any(ord(c) > 127 for c in key):
        raise ValueError("The key must contain only ASCII characters.")
    return "".join(format(ord(c), "08b") for c in key)


# ---------------------------------------------------------------
# Key schedule
# ---------------------------------------------------------------
def permute(bits, table):
    return "".join(bits[p - 1] for p in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def kplus_from_key(key):
    k64 = key_to_bits(key)
    return k64, permute(k64, PC1)


def round_key(kplus, i):
    """Return K_i and every intermediate step needed to obtain it."""
    c, d = kplus[:28], kplus[28:]
    steps = [(0, 0, c, d)]
    for n in range(1, i + 1):
        c, d = left_shift(c, SHIFTS[n - 1]), left_shift(d, SHIFTS[n - 1])
        steps.append((n, SHIFTS[n - 1], c, d))
    cd = c + d
    return {"C0": kplus[:28], "D0": kplus[28:], "steps": steps,
            "CD": cd, "K": permute(cd, PC2)}


# ---------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------
def group(bits, size):
    return " ".join(bits[i:i + size] for i in range(0, len(bits), size))


def to_hex(bits):
    return format(int(bits, 2), "0{}X".format(len(bits) // 4))
