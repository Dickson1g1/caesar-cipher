"""
Brute-force attack and frequency analysis for Caesar cipher.

Brute force works because the Caesar cipher has only 26 possible keys.
We try every shift (0-25), decrypt the ciphertext with each one, and rank
the results by how "English-like" the output looks.

Frequency analysis:
English text has a characteristic distribution of letter frequencies.
'e' is the most common (~12.7%), then 't', 'a', 'o', 'i', 'n', ...
By comparing the frequency distribution of a candidate plaintext to the
known English distribution, we can score how likely it is to be real English.

The scoring method used here is the Index of Coincidence (IoC) — summed
product of expected vs. observed frequencies. Higher score = more English-like.
"""

from .cipher import decrypt

# English letter frequencies (a-z) as decimals, from corpus analysis.
# Source: Lewand, R. (2000). Cryptological Mathematics.
# These are the probabilities that any given letter in an English text is
# each particular letter.
ENGLISH_FREQ = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
    'y': 0.01974, 'z': 0.00074,
}


def score_english(text: str) -> float:
    """
    Score how closely a string's letter frequencies match English.

    Algorithm:
    1. Count each letter in the text (case-insensitive).
    2. For each letter, multiply the observed fraction by the expected
       English frequency and sum the products.

    This is the chi-squared-adjacent "fitness" score. A higher score
    means the text looks more like English.

    A random string scores ~0.038 (uniform distribution over 26 letters).
    Real English scores ~0.065 (the Index of Coincidence for English).

    Parameters
    ----------
    text : str
        The candidate plaintext to score.

    Returns
    -------
    float
        A fitness score. Higher = more English-like.
    """
    # Extract only the alphabetic characters (lowercased) for analysis
    letters = [c.lower() for c in text if c.isalpha()]

    # If there are no letters, we can't score it — return 0
    if not letters:
        return 0.0

    total = len(letters)

    # Count occurrences of each letter
    counts = {}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1

    # Sum the product of (observed frequency) * (expected English frequency)
    # for each letter. Letters not in the text contribute 0.
    score = sum(
        (counts.get(letter, 0) / total) * expected_freq
        for letter, expected_freq in ENGLISH_FREQ.items()
    )
    return score


def brute_force(ciphertext: str) -> list[dict]:
    """
    Try all 26 possible Caesar shifts and rank results by English likelihood.

    Parameters
    ----------
    ciphertext : str
        The encrypted text to crack.

    Returns
    -------
    list[dict]
        A list of 26 dicts, sorted by score descending (most likely first).
        Each dict has:
          - 'shift'     : int  — the shift key tried
          - 'plaintext' : str  — the decrypted candidate
          - 'score'     : float — frequency analysis fitness score
          - 'rank'      : int  — 1 = most likely English
    """
    candidates = []

    # Try every possible shift value 0 through 25
    for shift in range(26):
        candidate = decrypt(ciphertext, shift)
        fitness   = score_english(candidate)
        candidates.append({
            "shift":     shift,
            "plaintext": candidate,
            "score":     fitness,
        })

    # Sort descending by score — the highest score is the best English match
    candidates.sort(key=lambda c: c["score"], reverse=True)

    # Add rank numbers (1 = most likely) after sorting
    for i, candidate in enumerate(candidates):
        candidate["rank"] = i + 1

    return candidates


def best_guess(ciphertext: str) -> dict:
    """
    Return the single most likely decryption based on frequency analysis.

    Parameters
    ----------
    ciphertext : str
        The encrypted text to crack.

    Returns
    -------
    dict
        The highest-scoring candidate from brute_force().
    """
    return brute_force(ciphertext)[0]
