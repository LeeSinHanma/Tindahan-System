import tkinter as tk

from db.database import init_database
from ui.app import App


def main() -> None:
	init_database()
	root = tk.Tk()
	App(root)
	root.mainloop()


if __name__ == "__main__":
	main()
