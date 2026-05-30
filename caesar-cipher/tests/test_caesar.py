import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from caesar.cipher   import encrypt, decrypt
from caesar.analysis import score_english, brute_force, best_guess


# ---------------------------------------------------------------------------
# cipher.py tests
# ---------------------------------------------------------------------------

def test_encrypt_basic():
    """Classic example: shift 3 turns Hello into Khoor."""
    assert encrypt("Hello", 3) == "Khoor"

def test_encrypt_full_sentence():
    assert encrypt("Hello, World!", 3) == "Khoor, Zruog!"

def test_encrypt_preserves_non_alpha():
    """Spaces, digits, punctuation must pass through unchanged."""
    assert encrypt("abc 123!", 1) == "bcd 123!"

def test_encrypt_wraps_around():
    """Z shifted by 1 should become A."""
    assert encrypt("Z", 1) == "A"
    assert encrypt("z", 1) == "a"

def test_encrypt_shift_zero():
    """Shift of 0 returns the original text unchanged."""
    assert encrypt("Hello", 0) == "Hello"

def test_encrypt_shift_26():
    """Shift of 26 is a full rotation — same as shift 0."""
    assert encrypt("Hello", 26) == "Hello"

def test_encrypt_large_shift():
    """Shifts > 25 are normalised via modulo 26."""
    assert encrypt("Hello", 29) == encrypt("Hello", 3)

def test_decrypt_reverses_encrypt():
    """decrypt(encrypt(text, k), k) must equal text for all k."""
    for shift in range(26):
        original = "The quick brown fox jumps over the lazy dog."
        assert decrypt(encrypt(original, shift), shift) == original

def test_decrypt_basic():
    assert decrypt("Khoor, Zruog!", 3) == "Hello, World!"

def test_case_preserved():
    """Uppercase stays uppercase, lowercase stays lowercase."""
    result = encrypt("AbCdEf", 1)
    assert result == "BcDeFg"


# ---------------------------------------------------------------------------
# analysis.py tests
# ---------------------------------------------------------------------------

def test_score_english_higher_for_english():
    """English text should score higher than a random-shifted version."""
    english = "The quick brown fox jumps over the lazy dog"
    # Shift by 7 to make it non-English looking
    shifted = encrypt(english, 7)
    assert score_english(english) > score_english(shifted)

def test_score_english_empty():
    """Empty string (no letters) returns 0."""
    assert score_english("") == 0.0
    assert score_english("12345!@#") == 0.0

def test_brute_force_finds_correct_shift():
    """
    For a clearly English plaintext, the best guess should recover
    the original message with the correct shift.
    """
    original  = "The quick brown fox jumps over the lazy dog"
    shift     = 13
    ciphertext = encrypt(original, shift)
    guess      = best_guess(ciphertext)
    assert guess["shift"]     == shift
    assert guess["plaintext"] == original

def test_brute_force_returns_26():
    """brute_force always returns exactly 26 candidates."""
    results = brute_force("hello")
    assert len(results) == 26

def test_brute_force_sorted():
    """Results must be sorted highest score first."""
    results = brute_force("Khoor Zruog")
    scores  = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)

def test_brute_force_ranks():
    """Rank 1 = index 0, rank 26 = index 25."""
    results = brute_force("hello")
    assert results[0]["rank"]  == 1
    assert results[25]["rank"] == 26


if __name__ == "__main__":
    tests  = [(k, v) for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✔ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✘ {name}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
