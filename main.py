import argparse
import tkinter as tk
from pathlib import Path

from ui.app import App


def main() -> None:
    parser = argparse.ArgumentParser(description="Tindahan POS and Inventory")
    parser.add_argument(
        "--smoke-test",
        type=Path,
        metavar="REPORT",
        help="check the bundle using a temporary database",
    )
    args = parser.parse_args()
    if args.smoke_test:
        from core.diagnostics import smoke_test

        smoke_test(args.smoke_test)
        return
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
