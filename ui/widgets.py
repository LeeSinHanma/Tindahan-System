"""Reusable controls for responsive desktop screens."""

import tkinter as tk
from tkinter import ttk

from . import theme


def page_header(parent, title, subtitle):
    header = ttk.Frame(parent)
    ttk.Label(header, text=title, style="Title.TLabel").pack(anchor="w")
    label = ttk.Label(header, text=subtitle, style="Muted.TLabel", wraplength=680)
    label.pack(anchor="w", pady=(4, 0))
    header.bind(
        "<Configure>", lambda e: label.configure(wraplength=max(200, e.width)), add="+"
    )
    return header


class ActionButton(ttk.Button):
    """Render shared button styles, accepting options from older dialogs."""

    def __init__(self, master, variant=None, **kwargs):
        color = kwargs.pop("bg", None)
        if variant is None:
            variant = (
                "Danger"
                if color in ("#dc2626", "#b91c1c")
                else "Primary"
                if color in ("#16a34a", "#059669", "#2563eb", "#1d4ed8")
                else ""
            )
        for key in (
            "fg",
            "activebackground",
            "activeforeground",
            "relief",
            "padx",
            "pady",
            "font",
            "anchor",
        ):
            kwargs.pop(key, None)
        kwargs.setdefault("style", f"{variant}.TButton" if variant else "TButton")
        kwargs.setdefault("cursor", "hand2")
        super().__init__(master, **kwargs)


class Tooltip:
    """Keep collapsed navigation labels available to mouse and keyboard users."""

    def __init__(self, widget, text):
        self.widget, self.text = widget, text
        self.timer = self.popup = None
        widget.bind("<Enter>", self.schedule, add="+")
        widget.bind("<FocusIn>", self.schedule, add="+")
        for event in ("<Leave>", "<FocusOut>", "<Destroy>", "<ButtonPress>"):
            widget.bind(event, self.hide, add="+")

    def schedule(self, event=None):
        self.hide()
        self.timer = self.widget.after(650, self.show)

    def show(self):
        self.timer = None
        if not self.widget.winfo_ismapped():
            return
        self.popup = tk.Toplevel(self.widget)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 8
        y = self.widget.winfo_rooty()
        self.popup.geometry(f"+{x}+{y}")
        ttk.Label(
            self.popup, text=self.text, padding=(10, 6), style="Panel.TLabel"
        ).pack()

    def hide(self, event=None):
        if self.timer is not None:
            self.widget.after_cancel(self.timer)
            self.timer = None
        if self.popup is not None:
            if self.popup.winfo_exists():
                self.popup.destroy()
            self.popup = None


class FlowFrame(ttk.Frame):
    """Wrap controls into additional rows instead of clipping actions."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.items = []
        self._pending = None
        self.bind("<Configure>", self._schedule)

    def add(self, widget):
        self.items.append(widget)
        widget.grid(
            row=0, column=len(self.items) - 1, sticky="w", padx=(0, 6), pady=(0, 6)
        )
        self._schedule()
        return widget

    def _schedule(self, event=None):
        if self._pending is None:
            self._pending = self.after_idle(self._layout)

    def _layout(self):
        self._pending = None
        width = max(self.winfo_width(), 1)
        row = col = used = 0
        for item in self.items:
            size = item.winfo_reqwidth() + 6
            if used and used + size > width:
                row, col, used = row + 1, 0, 0
            item.grid_configure(row=row, column=col)
            used += size
            col += 1

    def destroy(self):
        if self._pending is not None:
            self.after_cancel(self._pending)
        super().destroy()


class ScrollFrame(ttk.Frame):
    """Scroll long forms while keeping dialog actions outside the scroll area."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(
            self, background=theme.BG, highlightthickness=0, width=1, height=1
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.content = ttk.Frame(self.canvas, padding=16)
        self._window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self._window, width=e.width),
        )
        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self._scroll_tag = f"ScrollForm{id(self)}"
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_class(self._scroll_tag, sequence, self._wheel)
        self._bind_job = self.after_idle(self._bind_scroll)

    def _bind_scroll(self):
        self._bind_job = None

        def attach(widget):
            widget.bindtags((*widget.bindtags(), self._scroll_tag))
            for child in widget.winfo_children():
                attach(child)

        attach(self.content)

    def destroy(self):
        if self._bind_job is not None:
            self.after_cancel(self._bind_job)
        super().destroy()

    def _wheel(self, event):
        if self.content.winfo_height() > self.canvas.winfo_height():
            step = -1 if event.num == 4 or getattr(event, "delta", 0) > 0 else 1
            self.canvas.yview_scroll(step, "units")
            return "break"


class DataTable(ttk.Treeview):
    """Sortable table with empty states; values and row IDs stay intact."""

    def __init__(self, master, empty_text="No records to display.", **kwargs):
        kwargs.setdefault("selectmode", "browse")
        super().__init__(master, **kwargs)
        self.empty_text = empty_text
        self.empty_label = ttk.Label(
            self,
            text=empty_text,
            style="Empty.TLabel",
            anchor="center",
            justify="center",
        )
        self.bind("<Configure>", self._refresh_empty, add="+")
        self._refresh_empty()

    def _refresh_empty(self, event=None):
        if self.get_children():
            self.empty_label.place_forget()
        else:
            self.empty_label.configure(
                text=self.empty_text, wraplength=max(80, self.winfo_width() - 32)
            )
            self.empty_label.place(relx=0.5, y=52, anchor="n")

    def insert(self, *args, **kwargs):
        item = super().insert(*args, **kwargs)
        self._refresh_empty()
        return item

    def delete(self, *items):
        super().delete(*items)
        self._refresh_empty()

    def heading(self, column, option=None, **kwargs):
        if "text" in kwargs and "command" not in kwargs:
            kwargs["command"] = lambda c=column: self.sort_column(c)
        return super().heading(column, option, **kwargs)

    def sort_column(self, column, reverse=False):
        def key(item):
            value = self.set(item, column)
            try:
                return (0, float(value.replace("PHP", "").replace(",", "").strip()))
            except ValueError:
                return (1, value.casefold())

        for index, item in enumerate(
            sorted(self.get_children(), key=key, reverse=reverse)
        ):
            self.move(item, "", index)
        super().heading(column, command=lambda: self.sort_column(column, not reverse))


def table(
    parent,
    columns,
    headings,
    widths,
    *,
    empty_text="No records to display.",
    height=5,
    displaycolumns="#all",
):
    box = ttk.Frame(parent)
    box.columnconfigure(0, weight=1)
    box.rowconfigure(0, weight=1)
    tree = DataTable(
        box,
        columns=columns,
        show="headings",
        height=height,
        empty_text=empty_text,
        displaycolumns=displaycolumns,
    )
    for column, heading, width in zip(columns, headings, widths):
        tree.heading(column, text=heading)
        tree.column(
            column,
            width=width,
            minwidth=width,
            stretch=column in ("name", "product", "customer", "description", "k"),
        )
        if column in (
            "price",
            "total",
            "amount",
            "subtotal",
            "original_price",
            "sell_price",
            "revenue",
            "v",
        ):
            tree.column(column, anchor="e")
        elif column in ("qty", "stock", "pending", "count", "pick"):
            tree.column(column, anchor="center")
    visible = columns if displaycolumns == "#all" else displaycolumns
    if not any(tree.column(column, "stretch") for column in visible):
        flexible = next((c for c in ("date", "username") if c in visible), visible[0])
        tree.column(flexible, stretch=True)
    tree.grid(row=0, column=0, sticky="nsew")
    vertical = ttk.Scrollbar(box, orient="vertical", command=tree.yview)
    vertical.grid(row=0, column=1, sticky="ns")
    horizontal = ttk.Scrollbar(box, orient="horizontal", command=tree.xview)
    horizontal.grid(row=1, column=0, sticky="ew")
    tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
    return box, tree


class MetricGrid(ttk.Frame):
    """Cards reflow according to available width, rather than monitor size."""

    def __init__(self, master, specs):
        super().__init__(master)
        self.cards, self.values, self._columns = [], {}, 0
        for title, key in specs:
            card = ttk.Frame(self, style="Panel.TFrame", padding=14)
            ttk.Label(
                card,
                text=title,
                style="Panel.TLabel",
                foreground=theme.MUTED,
                font=(theme.FONT, 9),
            ).pack(anchor="w")
            value = ttk.Label(
                card, text="—", style="Metric.TLabel", font=(theme.FONT, 18, "bold")
            )
            value.pack(anchor="w", fill="x", pady=(6, 0))
            self.cards.append(card)
            self.values[key] = value
        self.bind("<Configure>", self._layout)

    def _layout(self, event):
        columns = min(len(self.cards), 4 if event.width >= 1100 else 2)
        if columns == self._columns:
            return
        for i in range(len(self.cards)):
            self.columnconfigure(i, weight=0, uniform="")
        for i, card in enumerate(self.cards):
            card.grid(
                row=i // columns,
                column=i % columns,
                sticky="nsew",
                padx=(0, 8),
                pady=(0, 8),
            )
        for i in range(columns):
            self.columnconfigure(i, weight=1, uniform="metric")
        self._columns = columns


class AdaptivePanels(ttk.Frame):
    """Use side-by-side panels on wide windows and tabs on smaller windows."""

    def __init__(self, master, breakpoint=1000):
        super().__init__(master)
        self.breakpoint = breakpoint
        self.panels = []
        self.notebook = ttk.Notebook(self)
        self.rowconfigure(0, weight=1)
        self._wide = None
        self._preferred = None
        self.bind("<Configure>", self._layout)

    def add(self, label):
        panel = ttk.Frame(self, padding=12)
        self.panels.append((label, panel))
        return panel

    def _layout(self, event):
        wide = event.width >= self.breakpoint
        if wide == self._wide:
            return
        self._wide = wide
        if wide:
            for tab in self.notebook.tabs():
                self.notebook.forget(tab)
            self.notebook.grid_remove()
            for i, (_, panel) in enumerate(self.panels):
                self.columnconfigure(i, weight=1, uniform="panel")
                panel.grid(
                    row=0, column=i, sticky="nsew", padx=(0, 12 if i == 0 else 0)
                )
        else:
            for i, (label, panel) in enumerate(self.panels):
                panel.grid_forget()
                self.columnconfigure(i, weight=0, uniform="")
                self.notebook.add(panel, text=label)
            self.columnconfigure(0, weight=1, uniform="")
            self.notebook.grid(row=0, column=0, sticky="nsew")
            if self._preferred is not None:
                self.notebook.select(self._preferred)

    def show(self, panel):
        self._preferred = panel
        if self._wide is False and str(panel) in self.notebook.tabs():
            self.notebook.select(panel)


def center_dialog(modal, width, height):
    parent = modal.master.winfo_toplevel()
    modal.update_idletasks()
    width = min(width, modal.winfo_screenwidth() - 32)
    height = min(height, modal.winfo_screenheight() - 80)
    x = max(
        0,
        min(
            parent.winfo_rootx() + (parent.winfo_width() - width) // 2,
            modal.winfo_screenwidth() - width,
        ),
    )
    y = max(
        0,
        min(
            parent.winfo_rooty() + (parent.winfo_height() - height) // 2,
            modal.winfo_screenheight() - height - 48,
        ),
    )
    modal.geometry(f"{width}x{height}+{x}+{y}")
    modal.bind("<Escape>", lambda event: modal.destroy())
