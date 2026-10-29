"""
Laboratory Work No. 3 - Cryptography and Security
Task 3.1: the Playfair cipher for messages in Romanian (31 letters).

The Romanian alphabet has 31 letters, so the encryption matrix is 5 x 6 = 30 cells.
As in the classic algorithm (where J is replaced by I), the rare letter J is replaced
by I, and the remaining 30 letters fill the matrix exactly. Used by gui.py.
"""

# Romanian alphabet (31 letters)
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "Ș", "T", "Ț", "U", "V", "W", "X", "Y", "Z"]
LOWER = ["a", "ă", "â", "b", "c", "d", "e", "f", "g", "h", "i", "î", "j", "k", "l",
         "m", "n", "o", "p", "q", "r", "s", "ș", "t", "ț", "u", "v", "w", "x", "y", "z"]

ROWS, COLS = 5, 6
MATRIX_LETTERS = [ch for ch in ALPHABET if ch != "J"]   # 30 letters, J -> I
FILLER = "X"            # inserted between double letters and at the end of an odd text
FILLER_FOR_X = "Q"      # used when the letter to separate is X itself

# Every accepted character -> its uppercase letter (cedilla forms Ş Ţ -> comma forms Ș Ț)
TO_UPPER = {}
for up, low in zip(ALPHABET, LOWER):
    TO_UPPER[up] = up
    TO_UPPER[low] = up
TO_UPPER.update({"Ş": "Ș", "ş": "Ș", "Ţ": "Ț", "ţ": "Ț"})

ALLOWED = "'A'–'Z', 'a'–'z' and the Romanian letters Ă Â Î Ș Ț (ă â î ș ț)"


# ---------------------------------------------------------------
# Validation
# ---------------------------------------------------------------
def normalize(text, allow_spaces=True):
    """Uppercase letters only, spaces removed, J replaced by I."""
    out = []
    for ch in text:
        if ch in " \n\t" and allow_spaces:
            continue
        if ch not in TO_UPPER:
            raise ValueError(f"Invalid character '{ch}'. Allowed characters: {ALLOWED}.")
        up = TO_UPPER[ch]
        out.append("I" if up == "J" else up)
    if not out:
        raise ValueError("The text must contain at least one letter.")
    return "".join(out)


def parse_key(key):
    """The key must have at least 7 letters and only allowed characters."""
    k = normalize(key)
    if len(k) < 7:
        raise ValueError(f"The key is too short ({len(k)} letters). It must have at least 7 letters.")
    return k


# ---------------------------------------------------------------
# a) Preparing the text
# ---------------------------------------------------------------
def filler_for(letter):
    return FILLER_FOR_X if letter == FILLER else FILLER


def prepare(text):
    """Split the text into pairs; a filler separates two equal letters
    of the same pair and completes a last single letter."""
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else None
        if b is None:
            pairs.append(a + filler_for(a))
            i += 1
        elif a == b:
            pairs.append(a + filler_for(a))
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs


# ---------------------------------------------------------------
# b) Building the encryption matrix
# ---------------------------------------------------------------
def unique_letters(key):
    """Remove repeated letters of the key, starting from the second occurrence."""
    seen = []
    for ch in key:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def build_matrix(key):
    order = unique_letters(key) + "".join(MATRIX_LETTERS)
    cells = unique_letters(order)
    return [list(cells[r * COLS:(r + 1) * COLS]) for r in range(ROWS)]


def positions(matrix):
    return {matrix[r][c]: (r, c) for r in range(ROWS) for c in range(COLS)}


# ---------------------------------------------------------------
# c) Encrypting / decrypting a pair
# ---------------------------------------------------------------
def transform_pair(pair, matrix, pos, step):
    """step = +1 for encryption, -1 for decryption."""
    (r1, c1), (r2, c2) = pos[pair[0]], pos[pair[1]]
    if r1 == r2:                                    # same row: next / previous letter in the row
        return matrix[r1][(c1 + step) % COLS] + matrix[r2][(c2 + step) % COLS]
    if c1 == c2:                                    # same column: letter below / above
        return matrix[(r1 + step) % ROWS][c1] + matrix[(r2 + step) % ROWS][c2]
    return matrix[r1][c2] + matrix[r2][c1]          # rectangle: same row, other column


def encrypt(message, key):
    matrix = build_matrix(parse_key(key))
    pos = positions(matrix)
    pairs = prepare(normalize(message))
    return matrix, pairs, [transform_pair(p, matrix, pos, +1) for p in pairs]


def decrypt(cryptogram, key):
    matrix = build_matrix(parse_key(key))
    pos = positions(matrix)
    text = normalize(cryptogram)
    if len(text) % 2:
        raise ValueError(f"A cryptogram must have an even number of letters (it has {len(text)}).")
    pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
    for p in pairs:
        if p[0] == p[1]:
            raise ValueError(f"The pair '{p}' has two equal letters, so it cannot come from Playfair encryption.")
    return matrix, pairs, [transform_pair(p, matrix, pos, -1) for p in pairs]
