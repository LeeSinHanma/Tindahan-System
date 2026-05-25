"""
Centralized theming and responsive sizing system for the POS application.
"""
import tkinter as tk


class Theme:
    """Centralized theme and sizing configuration."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize theme based on screen size."""
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        self.is_compact = screen_w < 1400 or screen_h < 820

    # ========== FONT SIZES ==========
    @property
    def title_large(self) -> int:
        """Large title (app headers)."""
        return 20 if self.is_compact else 24

    @property
    def title_medium(self) -> int:
        """Medium title (section headers)."""
        return 16 if self.is_compact else 18

    @property
    def title_small(self) -> int:
        """Small title (frame headers)."""
        return 14 if self.is_compact else 16

    @property
    def heading_large(self) -> int:
        """Large heading."""
        return 13 if self.is_compact else 14

    @property
    def heading_medium(self) -> int:
        """Medium heading."""
        return 12 if self.is_compact else 13

    @property
    def heading_small(self) -> int:
        """Small heading."""
        return 11 if self.is_compact else 12

    @property
    def body_large(self) -> int:
        """Large body text."""
        return 11 if self.is_compact else 12

    @property
    def body_medium(self) -> int:
        """Medium body text."""
        return 10 if self.is_compact else 11

    @property
    def body_small(self) -> int:
        """Small body text."""
        return 9 if self.is_compact else 10

    @property
    def metric_label(self) -> int:
        """Metric label font size."""
        return 9 if self.is_compact else 10

    @property
    def metric_value(self) -> int:
        """Metric value font size."""
        return 13 if self.is_compact else 16

    @property
    def button_font(self) -> int:
        """Button font size."""
        return 10 if self.is_compact else 11

    # ========== SPACING ==========
    @property
    def padding_large(self) -> int:
        """Large padding."""
        return 12 if self.is_compact else 16

    @property
    def padding_medium(self) -> int:
        """Medium padding."""
        return 8 if self.is_compact else 10

    @property
    def padding_small(self) -> int:
        """Small padding."""
        return 4 if self.is_compact else 6

    @property
    def padding_xs(self) -> int:
        """Extra small padding."""
        return 2 if self.is_compact else 3

    @property
    def gap_medium(self) -> int:
        """Medium gap between sections."""
        return 6 if self.is_compact else 8

    @property
    def gap_large(self) -> int:
        """Large gap between sections."""
        return 8 if self.is_compact else 12

    # ========== BUTTON SIZING ==========
    @property
    def button_padx_large(self) -> int:
        """Large button horizontal padding."""
        return 12 if self.is_compact else 16

    @property
    def button_padx_medium(self) -> int:
        """Medium button horizontal padding."""
        return 10 if self.is_compact else 12

    @property
    def button_padx_small(self) -> int:
        """Small button horizontal padding."""
        return 8 if self.is_compact else 10

    @property
    def button_pady_large(self) -> int:
        """Large button vertical padding."""
        return 8 if self.is_compact else 10

    @property
    def button_pady_medium(self) -> int:
        """Medium button vertical padding."""
        return 6 if self.is_compact else 8

    @property
    def button_pady_small(self) -> int:
        """Small button vertical padding."""
        return 4 if self.is_compact else 5

    # ========== TABLE/LIST SIZING ==========
    @property
    def table_rowheight(self) -> int:
        """Table row height."""
        return 22 if self.is_compact else 28

    @property
    def table_height_large(self) -> int:
        """Large table height (rows)."""
        return 12 if self.is_compact else 16

    @property
    def table_height_medium(self) -> int:
        """Medium table height (rows)."""
        return 8 if self.is_compact else 10

    @property
    def table_height_small(self) -> int:
        """Small table height (rows)."""
        return 4 if self.is_compact else 6

    @property
    def table_column_width_id(self) -> int:
        """ID column width."""
        return 45 if self.is_compact else 50

    @property
    def table_column_width_name(self) -> int:
        """Name column width."""
        return 160 if self.is_compact else 200

    @property
    def table_column_width_barcode(self) -> int:
        """Barcode column width."""
        return 100 if self.is_compact else 130

    @property
    def table_column_width_price(self) -> int:
        """Price column width."""
        return 70 if self.is_compact else 85

    @property
    def table_column_width_qty(self) -> int:
        """Quantity column width."""
        return 50 if self.is_compact else 60

    @property
    def table_column_width_status(self) -> int:
        """Status column width."""
        return 60 if self.is_compact else 70

    # ========== SIDEBAR ==========
    @property
    def sidebar_width(self) -> int:
        """Sidebar width."""
        return 280  # Fixed, not responsive

    # ========== CONTENT PADDING ==========
    @property
    def content_padding(self) -> int:
        """Main content padding."""
        return 12 if self.is_compact else 16


# Global theme instance (initialized by App)
_theme: Theme | None = None


def get_theme() -> Theme:
    """Get the global theme instance."""
    if _theme is None:
        raise RuntimeError("Theme not initialized. Call set_theme() first.")
    return _theme


def set_theme(theme: Theme) -> None:
    """Set the global theme instance."""
    global _theme
    _theme = theme
