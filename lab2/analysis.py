"""
Laboratory Work No. 2 - Cryptography and Security
Cryptanalysis of monoalphabetic ciphers: frequency analysis helpers.
Used by gui.py. Only letters are encrypted; every other character stays as it is.
"""

from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Table 2.2 - letter frequencies of the English language (%)
ENGLISH_FREQ = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23, "G": 2.01,
    "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75,
    "O": 7.51, "P": 1.93, "Q": 0.09, "R": 5.99, "S": 6.33, "T": 9.06, "U": 2.76,
    "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07,
}
ENGLISH_ORDER = sorted(ENGLISH_FREQ, key=ENGLISH_FREQ.get, reverse=True)


def letters(text):
    """Only the Latin letters of the text, in uppercase."""
    return [ch.upper() for ch in text if ch.upper() in ALPHABET]


def frequencies(text):
    """Return {letter: (count, percent)} for all 26 letters."""
    found = letters(text)
    total = len(found) or 1
    cnt = Counter(found)
    return {ch: (cnt[ch], 100 * cnt[ch] / total) for ch in ALPHABET}


def sorted_by_frequency(freq):
    """Letters in decreasing order of frequency (ties in alphabetical order)."""
    return sorted(ALPHABET, key=lambda ch: (-freq[ch][0], ch))


def ngrams(text, n, top=10):
    """Most frequent letter n-grams that stay inside one word."""
    cnt = Counter()
    for word in "".join(ch.upper() if ch.isalpha() else " " for ch in text).split():
        for i in range(len(word) - n + 1):
            cnt[word[i:i + n]] += 1
    return cnt.most_common(top)


def words_of_length(text, n, top=10):
    """Most frequent cipher words that have exactly n letters."""
    cnt = Counter(w for w in "".join(ch.upper() if ch.isalpha() else " " for ch in text).split()
                  if len(w) == n)
    return cnt.most_common(top)


def frequency_guess(freq):
    """Initial key: the i-th most frequent cipher letter -> the i-th most frequent English letter."""
    return dict(zip(sorted_by_frequency(freq), ENGLISH_ORDER))


def apply_key(text, key):
    """Replace the cipher letters found in `key` (cipher -> plain).

    As in the lab example, a recovered letter is written in lowercase and a
    cipher letter that is not solved yet stays in UPPERCASE, so the two can be
    told apart while the text is being broken.
    """
    out = []
    for ch in text:
        up = ch.upper()
        if up in ALPHABET:
            out.append(key[up].lower() if key.get(up) else up)
        else:
            out.append(ch)
    return "".join(out)


def decrypt(text, key):
    """Final decryption that keeps the original letter case."""
    out = []
    for ch in text:
        up = ch.upper()
        if up in ALPHABET and key.get(up):
            plain = key[up]
            out.append(plain if ch.isupper() else plain.lower())
        else:
            out.append(ch)
    return "".join(out)


def check_key(key):
    """Return an error message if two cipher letters map to the same plain letter."""
    used = {}
    for c, p in key.items():
        if not p:
            continue
        if len(p) != 1 or p.upper() not in ALPHABET:
            return f"'{p}' is not a letter (cipher letter {c})."
        p = p.upper()
        if p in used:
            return f"Plain letter {p} is used twice: for {used[p]} and for {c}."
        used[p] = c
    return None
