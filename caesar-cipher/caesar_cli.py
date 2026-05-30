#!/usr/bin/env python3
"""
caesar_cli.py — Caesar cipher CLI tool.

Three subcommands:
  encrypt   Encrypt plaintext with a shift key
  decrypt   Decrypt ciphertext with the original shift key
  crack     Brute-force all 26 shifts ranked by English frequency
"""

import argparse
import sys
from caesar.cipher   import encrypt, decrypt
from caesar.analysis import brute_force, best_guess
from caesar.display  import (print_result, print_brute_force,
                              print_error, print_alphabet_table, console)


def cmd_encrypt(args) -> int:
    """Encrypt the given text with the specified shift."""
    ciphertext = encrypt(args.text, args.shift)
    print_result("encrypt", args.text, ciphertext, args.shift)

    # Optionally show the full substitution alphabet for educational context
    if args.show_table:
        print_alphabet_table(args.shift)

    # If --output-only flag is set, also print the bare ciphertext to stdout
    # so the result can be piped: caesar_cli.py encrypt "hello" 3 --output-only | ...
    if args.output_only:
        print(ciphertext)

    return 0


def cmd_decrypt(args) -> int:
    """Decrypt the given ciphertext with the specified shift."""
    plaintext = decrypt(args.text, args.shift)
    print_result("decrypt", args.text, plaintext, args.shift)

    if args.output_only:
        print(plaintext)

    return 0


def cmd_crack(args) -> int:
    """
    Brute-force all 26 shifts and rank by English frequency analysis.

    Displays the top N candidates and highlights the best guess.
    Returns exit code 0 always — 'cracking' never technically fails.
    """
    candidates = brute_force(args.text)
    print_brute_force(candidates, top_n=args.top)

    if args.output_only:
        # Print just the best guess plaintext for scripting
        print(candidates[0]["plaintext"])

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="caesar",
        description="Caesar cipher — encrypt, decrypt, and brute-force crack.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  caesar encrypt "Hello World" 13
  caesar decrypt "Uryyb Jbeyq" 13
  caesar crack "Khoor, Zruog!"
  caesar encrypt "secret" 7 --show-table
  caesar crack "Wkh txlfn eurzq ira" --top 5
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- encrypt subcommand ---
    enc = subparsers.add_parser("encrypt", help="Encrypt plaintext with a shift key")
    enc.add_argument("text",  type=str, help="Plaintext to encrypt")
    enc.add_argument("shift", type=int, help="Shift amount (0-25)")
    enc.add_argument("--show-table",  action="store_true",
                     help="Show the full A-Z substitution alphabet")
    enc.add_argument("--output-only", action="store_true",
                     help="Also print bare ciphertext to stdout (for piping)")

    # --- decrypt subcommand ---
    dec = subparsers.add_parser("decrypt", help="Decrypt ciphertext with the original key")
    dec.add_argument("text",  type=str, help="Ciphertext to decrypt")
    dec.add_argument("shift", type=int, help="Original shift amount (0-25)")
    dec.add_argument("--output-only", action="store_true",
                     help="Also print bare plaintext to stdout (for piping)")

    # --- crack subcommand ---
    crk = subparsers.add_parser("crack", help="Brute-force all 26 shifts")
    crk.add_argument("text", type=str, help="Ciphertext to crack")
    crk.add_argument("--top", type=int, default=10,
                     help="Number of top candidates to display (default 10)")
    crk.add_argument("--output-only", action="store_true",
                     help="Print only the best guess plaintext to stdout")

    return parser


def main() -> int:
    parser = build_parser()
    args   = parser.parse_args()

    # Validate shift values for encrypt/decrypt
    if args.command in ("encrypt", "decrypt"):
        if not (0 <= args.shift <= 25):
            print_error(f"Shift must be between 0 and 25, got {args.shift}")
            return 1

    commands = {
        "encrypt": cmd_encrypt,
        "decrypt": cmd_decrypt,
        "crack":   cmd_crack,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
