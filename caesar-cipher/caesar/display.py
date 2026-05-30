"""
Terminal rendering using the rich library.

All print() calls are banned from cipher.py and analysis.py — keeping
business logic and presentation separate makes each layer independently
testable and reusable.
"""

from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.text    import Text
from rich         import box

console = Console()


def print_result(mode: str, input_text: str, output_text: str, shift: int) -> None:
    """
    Display the result of a single encrypt or decrypt operation.

    Shows the input, the shift key, and the output in a clean panel.
    Color-codes the mode label: green for encrypt, blue for decrypt.
    """
    mode_color = "bold green" if mode == "encrypt" else "bold blue"

    # Build a two-column key-value table for the result details
    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column("key",   style="dim",  no_wrap=True)
    table.add_column("value", style="bold")

    table.add_row("mode",   Text(mode, style=mode_color))
    table.add_row("shift",  str(shift))
    table.add_row("input",  input_text)
    table.add_row("output", Text(output_text, style="bold cyan"))

    console.print(Panel(
        table,
        title=f"[{mode_color}] Caesar Cipher — {mode.capitalize()}[/{mode_color}]",
        border_style="dim",
    ))
    console.print()


def print_brute_force(candidates: list[dict], top_n: int = 10) -> None:
    """
    Display the top N brute-force candidates in a ranked table.

    Columns: rank, shift, score, and the first 60 characters of the plaintext.
    The top result (rank 1) is highlighted in green — the most likely plaintext.

    Parameters
    ----------
    candidates : list[dict]
        Sorted output from analysis.brute_force() — rank 1 first.
    top_n : int
        How many rows to display (default 10 — showing all 26 is noisy).
    """
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        padding=(0, 1),
        title="[bold]Brute Force Results — ranked by English frequency score[/bold]",
        title_style="dim",
    )

    table.add_column("Rank",      style="dim",  width=6,  justify="right")
    table.add_column("Shift",     style="bold", width=7,  justify="center")
    table.add_column("Score",     style="dim",  width=8,  justify="right")
    table.add_column("Plaintext preview",        min_width=40)

    for candidate in candidates[:top_n]:
        rank      = candidate["rank"]
        shift     = candidate["shift"]
        score     = candidate["score"]
        # Truncate long plaintexts so the table doesn't overflow the terminal
        preview   = candidate["plaintext"][:60]
        if len(candidate["plaintext"]) > 60:
            preview += "…"

        # Highlight rank 1 (best guess) in green; others in default color
        if rank == 1:
            row_style = "bold green"
            rank_str  = "★ 1"
        else:
            row_style = ""
            rank_str  = str(rank)

        table.add_row(
            Text(rank_str,         style=row_style),
            Text(str(shift),       style=row_style),
            Text(f"{score:.4f}",   style=row_style),
            Text(preview,          style=row_style),
        )

    console.print(table)
    console.print()

    # Print the best guess in a separate panel so it stands out
    best = candidates[0]
    console.print(Panel(
        Text(best["plaintext"], style="bold cyan"),
        title=f"[bold green]Best guess — shift {best['shift']} "
              f"(score {best['score']:.4f})[/bold green]",
        border_style="green",
    ))
    console.print()


def print_error(message: str) -> None:
    """Print an error message to the console in red."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_alphabet_table(shift: int) -> None:
    """
    Display a visual mapping of plaintext → ciphertext alphabet for a given shift.
    Helps the user understand exactly what substitution a particular shift produces.

    Example for shift=3:
      Plain:  A B C D E F G ... Z
      Cipher: D E F G H I J ... C
    """
    from .cipher import encrypt

    plain  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = encrypt(plain, shift)

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim",
                  title=f"[dim]Alphabet substitution table — shift {shift}[/dim]")

    # One column per letter — 26 narrow columns
    for letter in plain:
        table.add_column(letter, justify="center", width=3)

    table.add_row(*list(cipher), style="bold cyan")

    console.print(table)
    console.print()
