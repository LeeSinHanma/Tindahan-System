"""
ThemeManager: Centralized theme and sizing configuration.
Provides responsive font sizes, padding, gaps, and heights based on screen layout.
"""


class ThemeManager:
    """
    Manages UI theme properties (fonts, spacing, dimensions) based on layout mode.
    Supports compact and normal layouts for different screen sizes.
    """

    def __init__(self, compact_layout: bool = False) -> None:
        """
        Initialize ThemeManager with layout mode.

        Args:
            compact_layout: If True, use smaller sizes for limited screen space (< 1400x820).
        """
        self.compact_layout = compact_layout

    # Font Sizes
    @property
    def heading_huge(self) -> int:
        """Largest heading size (page title)."""
        return 20 if self.compact_layout else 24

    @property
    def heading_large(self) -> int:
        """Large heading size."""
        return 14 if self.compact_layout else 16

    @property
    def body_medium(self) -> int:
        """Medium body text and label size."""
        return 10 if self.compact_layout else 11

    @property
    def body_small(self) -> int:
        """Small body text size."""
        return 9 if self.compact_layout else 10

    @property
    def monospace_medium(self) -> int:
        """Monospace font size for input fields (barcode scanner, etc)."""
        return 11 if self.compact_layout else 14

    # Padding and Spacing
    @property
    def padding_medium(self) -> int:
        """Standard padding inside containers."""
        return 6 if self.compact_layout else 10

    @property
    def gap_small(self) -> int:
        """Small gap between elements."""
        return 2 if self.compact_layout else 4

    @property
    def gap_medium(self) -> int:
        """Standard gap between sections."""
        return 6 if self.compact_layout else 8

    @property
    def gap_large(self) -> int:
        """Large gap between major sections."""
        return 8 if self.compact_layout else 12

    # Button Styling
    @property
    def button_padding_x(self) -> int:
        """Horizontal padding for buttons."""
        return 8 if self.compact_layout else 10

    @property
    def button_padding_y(self) -> int:
        """Vertical padding for buttons."""
        return 4 if self.compact_layout else 5

    # Table Configuration
    @property
    def table_row_height(self) -> int:
        """Height of table rows."""
        return 22 if self.compact_layout else 28

    @property
    def table_height_small(self) -> int:
        """Small table height (3-5 rows visible)."""
        return 3 if self.compact_layout else 5

    @property
    def table_height_medium(self) -> int:
        """Medium table height (6-10 rows visible)."""
        return 6 if self.compact_layout else 10

    @property
    def table_height_large(self) -> int:
        """Large table height (12-16 rows visible)."""
        return 12 if self.compact_layout else 16

    @property
    def table_column_width_id(self) -> int:
        """Width for ID columns."""
        return 45

    @property
    def table_column_width_name(self) -> int:
        """Width for product name columns."""
        return 200 if self.compact_layout else 220

    @property
    def table_column_width_price(self) -> int:
        """Width for price columns."""
        return 70

    @property
    def table_column_width_qty(self) -> int:
        """Width for quantity columns."""
        return 50

    @property
    def table_column_width_status(self) -> int:
        """Width for status columns."""
        return 70

    # Chart Configuration
    @property
    def chart_height(self) -> int:
        """Height of chart elements."""
        return 120 if self.compact_layout else 170
