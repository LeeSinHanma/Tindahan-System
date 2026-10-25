"""Shared visual tokens and ttk styles for the desktop application."""

import tkinter.font as tkfont
from tkinter import ttk

BG = "#f3f5fa"
SURFACE = "#ffffff"
TEXT = "#172033"
MUTED = "#64748b"
BORDER = "#dfe5ef"
PRIMARY = "#2563eb"
NAV = "#111c32"
FONT = "sans-serif"


class Theme:
    """One sizing vocabulary, with aliases for existing screen builders."""

    def __init__(self, root=None, compact_layout=False):
        self.is_compact = root if isinstance(root, bool) else compact_layout

    compact_layout = property(
        lambda self: self.is_compact,
        lambda self, value: setattr(self, "is_compact", value),
    )
    title_large = heading_huge = property(lambda self: 22)
    title_medium = title_small = heading_large = property(lambda self: 14)
    heading_medium = heading_small = body_large = body_medium = property(
        lambda self: 10
    )
    body_small = metric_label = button_font = property(lambda self: 9)
    metric_value = property(lambda self: 22)
    monospace_medium = property(lambda self: 12)
    padding_large = content_padding = property(lambda self: 16)
    padding_medium = property(lambda self: 12)
    padding_small = gap_medium = property(lambda self: 8)
    padding_xs = gap_small = property(lambda self: 4)
    gap_large = property(lambda self: 16)
    button_padx_large = button_padx_medium = button_padx_small = button_padding_x = (
        property(lambda self: 12)
    )
    button_pady_large = button_pady_medium = button_pady_small = button_padding_y = (
        property(lambda self: 7)
    )
    table_rowheight = table_row_height = property(lambda self: 32)
    table_height_large = property(lambda self: 10)
    table_height_medium = property(lambda self: 6)
    table_height_small = property(lambda self: 3)
    table_column_width_id = property(lambda self: 44)
    table_column_width_name = property(lambda self: 190)
    table_column_width_barcode = property(lambda self: 145)
    table_column_width_price = property(lambda self: 85)
    table_column_width_qty = property(lambda self: 50)
    table_column_width_status = property(lambda self: 86)
    chart_height = property(lambda self: 155)
    sidebar_width = property(lambda self: 220)


def configure_styles(root):
    global FONT
    families = set(tkfont.families(root))
    FONT = next(
        (n for n in ("Inter", "Segoe UI", "Noto Sans", "DejaVu Sans") if n in families),
        "sans-serif",
    )
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
        tkfont.nametofont(name).configure(family=FONT, size=10)
    root.option_add("*Background", BG)
    root.option_add("*Foreground", TEXT)
    root.configure(background=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", font=(FONT, 10), background=BG, foreground=TEXT)
    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=SURFACE)
    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Panel.TLabel", background=SURFACE)
    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("Title.TLabel", font=(FONT, 22, "bold"))
    style.configure("Section.TLabel", font=(FONT, 12, "bold"))
    style.configure("Metric.TLabel", background=SURFACE, font=(FONT, 22, "bold"))
    style.configure(
        "Empty.TLabel", background=SURFACE, foreground=MUTED, font=(FONT, 10)
    )
    style.configure(
        "TLabelframe",
        background=SURFACE,
        bordercolor=BORDER,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelframe.Label", background=BG, foreground=MUTED, font=(FONT, 10, "bold")
    )
    style.configure(
        "TEntry",
        fieldbackground=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER,
        padding=(10, 7),
    )
    style.map(
        "TEntry", bordercolor=[("focus", PRIMARY)], lightcolor=[("focus", PRIMARY)]
    )
    style.configure("TCombobox", fieldbackground=SURFACE, padding=(8, 6), arrowsize=14)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", SURFACE)],
        selectbackground=[("readonly", SURFACE)],
        selectforeground=[("readonly", TEXT)],
    )
    style.configure("TCheckbutton", background=BG, padding=(0, 4))
    style.map("TCheckbutton", background=[("active", BG)])
    style.configure(
        "TButton",
        background=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER,
        padding=(12, 8),
        font=(FONT, 9, "bold"),
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", "#edf2fa"), ("pressed", "#dbe7ff")],
        bordercolor=[("focus", PRIMARY)],
        foreground=[("disabled", "#94a3b8")],
    )
    for name, background, foreground, hover in [
        ("Primary", PRIMARY, "white", "#1d4ed8"),
        ("Danger", "#fff1f2", "#be123c", "#ffe4e6"),
        ("Quiet", BG, MUTED, "#e8edf5"),
    ]:
        style.configure(
            f"{name}.TButton",
            background=background,
            foreground=foreground,
            bordercolor=background,
        )
        style.map(
            f"{name}.TButton",
            background=[("disabled", "#e8edf5"), ("pressed", hover), ("active", hover)],
            foreground=[("disabled", "#94a3b8"), ("!disabled", foreground)],
        )
    style.configure(
        "Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT,
        rowheight=32,
        borderwidth=0,
        font=(FONT, 10),
    )
    style.configure(
        "Treeview.Heading",
        background="#edf1f8",
        foreground=MUTED,
        relief="flat",
        padding=(8, 9),
        font=(FONT, 9, "bold"),
    )
    style.map(
        "Treeview",
        background=[("selected", "#dbeafe")],
        foreground=[("selected", "#1e40af")],
    )
    style.map("Treeview.Heading", background=[("active", "#e2e8f0")])
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(16, 9), background=BG)
    style.map(
        "TNotebook.Tab",
        background=[("selected", SURFACE)],
        foreground=[("selected", PRIMARY)],
    )
    for direction in ("Vertical", "Horizontal"):
        style.configure(
            f"{direction}.TScrollbar",
            background="#cbd5e1",
            troughcolor=BG,
            borderwidth=0,
            arrowsize=12,
        )


_theme = None


def get_theme():
    if _theme is None:
        raise RuntimeError("Theme not initialized. Call set_theme() first.")
    return _theme


def set_theme(theme):
    global _theme
    _theme = theme
