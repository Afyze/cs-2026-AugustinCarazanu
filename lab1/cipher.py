"""
Laboratory Work No. 1 - Cryptography and Security
Cipher logic: Caesar cipher and Caesar cipher with a keyword permutation
over the Romanian alphabet (n = 31). Used by gui.py.
"""

# ---------------------------------------------------------------
# Letter encoding (Table 2): A = 0, Ă = 1, ..., Z = 30
# ---------------------------------------------------------------
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I",
            "Î", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
            "Ș", "T", "Ț", "U", "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)                      # 31

LOWER = ["a", "ă", "â", "b", "c", "d", "e", "f", "g", "h", "i",
         "î", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
         "ș", "t", "ț", "u", "v", "w", "x", "y", "z"]

# Any accepted character -> its uppercase Romanian letter
TO_UPPER = {}
for up, low in zip(ALPHABET, LOWER):
    TO_UPPER[up] = up
    TO_UPPER[low] = up
# Cedilla variants (Ş ş Ţ ţ) are treated as comma-below letters (Ș ș Ț ț)
TO_UPPER.update({"Ş": "Ș", "ş": "Ș", "Ţ": "Ț", "ţ": "Ț"})

ALLOWED_TEXT = "Romanian letters (A-Z, Ă, Â, Î, Ș, Ț; any case) and spaces"


# ---------------------------------------------------------------
# Normalisation and validation
# ---------------------------------------------------------------
def normalize(text, allow_spaces=True):
    """Return the text in uppercase without spaces.
    Raises ValueError naming the first rejected character."""
    result = []
    for ch in text:
        if ch == " " and allow_spaces:
            continue
        if ch not in TO_UPPER:
            raise ValueError(f"Invalid character '{ch}'. Allowed: {ALLOWED_TEXT}.")
        result.append(TO_UPPER[ch])
    if not result:
        raise ValueError("The text must contain at least one letter.")
    return "".join(result)


def parse_key(value):
    """Key 1: an integer from 1 to 30."""
    value = value.strip()
    if not (value.isdigit() or (value.startswith("-") and value[1:].isdigit())):
        raise ValueError(f"Invalid key '{value}'. The key must be an integer from 1 to {N - 1}.")
    k = int(value)
    if not 1 <= k <= N - 1:
        raise ValueError(f"Invalid key {k}. The key must be an integer from 1 to {N - 1}.")
    return k


def parse_keyword(value):
    """Key 2: only Romanian letters, at least 7 characters."""
    value = value.strip()
    for ch in value:
        if ch not in TO_UPPER:
            raise ValueError(f"Invalid character '{ch}' in keyword. "
                             f"The keyword may contain only letters of the Romanian alphabet.")
    if len(value) < 7:
        raise ValueError(f"The keyword is too short ({len(value)} characters). "
                         f"It must have at least 7 letters.")
    return "".join(TO_UPPER[ch] for ch in value)


# ---------------------------------------------------------------
# Building the permuted alphabet (Task 1.2)
# ---------------------------------------------------------------
def permuted_alphabet(keyword):
    """Distinct keyword letters first, then the remaining letters in natural order."""
    result = []
    for ch in keyword + "".join(ALPHABET):
        if ch not in result:
            result.append(ch)
    return result


# ---------------------------------------------------------------
# Encryption / decryption
# ---------------------------------------------------------------
def encrypt(text, k, alphabet=ALPHABET):
    index = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[(index[ch] + k) % N] for ch in text)


def decrypt(text, k, alphabet=ALPHABET):
    index = {letter: i for i, letter in enumerate(alphabet)}
    # Python's % is always non-negative; the extra + N keeps the formula
    # correct in languages whose remainder can be negative.
    return "".join(alphabet[(index[ch] - k + N) % N] for ch in text)
