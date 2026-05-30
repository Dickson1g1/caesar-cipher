"""
Caesar cipher core — encrypt and decrypt functions.

The Caesar cipher works by shifting every letter in the alphabet by a fixed
number of positions. For example with shift=3:
  A -> D,  B -> E,  Z -> C  (wraps around using modulo 26)

Non-alphabetic characters (spaces, digits, punctuation) are passed through
unchanged — only A-Z and a-z are shifted.

Historical note: Julius Caesar reportedly used a shift of 3 to communicate
with his generals. Today it is used purely as a teaching cipher — it offers
zero real security because there are only 26 possible keys.
"""


def _shift_char(char: str, shift: int) -> str:
    """
    Shift a single character by `shift` positions within its alphabet case.

    We use ord() to get the ASCII code of the character, subtract the base
    ('A' = 65 for uppercase, 'a' = 97 for lowercase) to get a 0-25 index,
    add the shift, apply modulo 26 to wrap around, then add the base back.

    Example: shift_char('Z', 3)
      ord('Z') = 90
      90 - 65 = 25        (position in alphabet)
      (25 + 3) % 26 = 2   (wraps: Z -> C)
      65 + 2 = 67 = 'C'
    """
    if char.isupper():
        base = ord('A')
    elif char.islower():
        base = ord('a')
    else:
        # Not a letter — return unchanged (spaces, digits, punctuation)
        return char

    return chr((ord(char) - base + shift) % 26 + base)


def encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt plaintext using a Caesar cipher with the given shift key.

    Parameters
    ----------
    plaintext : str
        The message to encrypt. May contain any characters.
    shift : int
        The shift amount (0-25). Values outside this range are normalised
        via modulo 26 so encrypt("hello", 29) == encrypt("hello", 3).

    Returns
    -------
    str
        The encrypted ciphertext. Same length as input; non-alpha chars
        are passed through unchanged.

    Examples
    --------
    >>> encrypt("Hello, World!", 3)
    'Khoor, Zruog!'
    >>> encrypt("abc", 1)
    'bcd'
    """
    # Normalise shift so any integer works (e.g. shift=29 becomes shift=3)
    shift = shift % 26
    # Apply _shift_char to every character and join the results
    return "".join(_shift_char(c, shift) for c in plaintext)


def decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt a Caesar-encrypted ciphertext using the original shift key.

    Decryption is simply encryption with the inverse shift.
    shift=3 forward, shift=-3 (or equivalently 23) backward.

    Parameters
    ----------
    ciphertext : str
        The encrypted message to decrypt.
    shift : int
        The shift that was used to encrypt (0-25).

    Returns
    -------
    str
        The recovered plaintext.

    Examples
    --------
    >>> decrypt("Khoor, Zruog!", 3)
    'Hello, World!'
    """
    # Decrypting with shift k is the same as encrypting with shift (26 - k)
    return encrypt(ciphertext, -shift)
