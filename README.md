```
  ██████╗ █████╗ ███████╗███████╗ █████╗ ██████╗ 
 ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗
 ██║     ███████║█████╗  ███████╗███████║██████╔╝
 ██║     ██╔══██║██╔══╝  ╚════██║██╔══██║██╔══██╗
 ╚██████╗██║  ██║███████╗███████║██║  ██║██║  ██║
  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

  ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ 
 ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
 ██║     ██║██████╔╝███████║█████╗  ██████╔╝
 ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
 ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
  ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

  encrypt · decrypt · brute force · frequency analysis
```

# caesar-cipher

> A Caesar cipher CLI tool — encrypt, decrypt, and brute-force crack
> ciphertext using frequency analysis. Clean Rich terminal output with
> colored tables and substitution alphabet visualisation.

---

## What it does

`caesar-cipher` implements the classical Caesar substitution cipher as a
command-line tool with three modes. Encrypt any message with a shift key,
decrypt it back, or crack an unknown ciphertext by testing all 26 possible
shifts and ranking results by how closely each candidate matches the
statistical letter frequencies of real English text.

```
$ python caesar_cli.py encrypt "Hello, World!" 3

╭─── Caesar Cipher — Encrypt ───╮
│  mode   encrypt                │
│  shift  3                      │
│  input  Hello, World!          │
│  output Khoor, Zruog!          │
╰────────────────────────────────╯

$ python caesar_cli.py crack "Khoor, Zruog!"

 Rank  Shift  Score   Plaintext preview
 ★ 1     3   0.0742  Hello, World!
   2    16   0.0401  Uryyb, Jbeyq!
   3     9   0.0398  Qbiil, Tloia!
   ...
```

---

## Features

- **Encrypt** — shift any text by a key from 0 to 25; non-alphabetic
  characters (spaces, punctuation, digits) are preserved unchanged
- **Decrypt** — recover the original message with the same key used to encrypt
- **Brute force crack** — try all 26 shifts automatically; rank every
  candidate by English letter frequency fitness score
- **Frequency analysis** — scores candidates using the Index of Coincidence
  method against the IANA-standard English letter frequency table
- **Substitution alphabet table** — `--show-table` flag displays the full
  A→Z plaintext to ciphertext mapping for any shift
- **Rich colored output** — tables, panels, and highlighted best-guess results
  via the `rich` library
- **Pipe-friendly** — `--output-only` flag prints just the result text to
  stdout for use in shell pipelines
- **ROT13 support** — shift 13 is its own inverse; `encrypt(encrypt(x,13),13) == x`

---

## Requirements

- Python 3.10+
- [`rich`](https://github.com/Textualize/rich)

```bash
pip install rich
```

---

## Installation

```bash
git clone https://github.com/Dickson1g1/caesar-cipher.git
cd caesar-cipher
python3 -m venv .venv && source .venv/bin/activate
pip install rich
chmod +x caesar_cli.py

# Optional: install system-wide
ln -s "$(pwd)/caesar_cli.py" ~/.local/bin/caesar
```

---

## Usage

```bash
# Encrypt
caesar encrypt "Hello, World!" 3
caesar encrypt "Hello, World!" 13        # ROT13

# Show the full A-Z substitution alphabet
caesar encrypt "secret" 7 --show-table

# Decrypt (key must be known)
caesar decrypt "Khoor, Zruog!" 3

# Brute-force crack (key unknown)
caesar crack "Khoor, Zruog!"

# Show only the top 5 candidates
caesar crack "Wkh txlfn eurzq ira" --top 5

# Pipe just the ciphertext to a file
caesar encrypt "top secret" 17 --output-only > encrypted.txt

# Crack from a file
caesar crack "$(cat encrypted.txt)" --output-only
```

---

## How frequency analysis works

The Caesar cipher has only 26 possible keys — small enough to try all of
them in microseconds. To automatically identify the correct one, each
candidate plaintext is scored against the known letter frequency distribution
of English (e.g. 'e' appears ~12.7% of the time, 't' ~9.1%, etc.).

The score is the sum of `observed_frequency × expected_frequency` for each
letter — a variant of the Index of Coincidence. Real English text scores
around 0.065; random text scores around 0.038. The shift producing the
highest score is almost always the correct key for any text longer than
~20 characters.

---

## Project structure

```
caesar-cipher/
├── caesar/
│   ├── __init__.py
│   ├── cipher.py       # encrypt() and decrypt() — pure functions
│   ├── analysis.py     # brute_force(), score_english(), best_guess()
│   └── display.py      # rich table and panel rendering
├── caesar_cli.py       # CLI entrypoint (encrypt / decrypt / crack)
└── tests/
    └── test_caesar.py
```

---

## Running tests

```bash
python tests/test_caesar.py
```

All tests are pure-function unit tests — no terminal output, no files.

---

## Concepts covered

- Modular arithmetic for alphabet wrapping (`ord()`, `chr()`, `% 26`)
- Pure function design — cipher logic fully separated from I/O
- Statistical text analysis (Index of Coincidence / frequency scoring)
- `argparse` subcommands for multi-mode CLI tools
- `rich` library — `Table`, `Panel`, `Text`, `Console`

---

## License

MIT — do whatever you want, attribution appreciated.
