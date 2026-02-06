# styles/styles.py
"""
Centralized styles for the MG Tools application.
"""
import customtkinter as ctk

class Style:
    # Colors - Background
    BG_PRIMARY = "#000000"      # Main window background
    BG_SECONDARY = "#111111"    # Frame background
    BG_TERTIARY = "#1a1a1a"     # Input fields, dark areas
    
    # Colors - Borders
    BORDER_LIGHT = "#222222"    # Light borders
    BORDER_MEDIUM = "#333333"   # Medium borders
    BORDER_DARK = "#444444"     # Dark borders
    
    # Colors - Text
    TEXT_PRIMARY = "#e0e0e0"    # Primary text
    TEXT_SECONDARY = "#888888"  # Secondary text
    TEXT_SUCCESS = "#27ae60"    # Success messages
    TEXT_ERROR = "#e74c3c"      # Error messages
    TEXT_WARNING = "#f39c12"    # Warning messages
    TEXT_INFO = "#3498db"       # Info messages
    
    # Colors - Buttons
    BTN_PRIMARY = "#2a2a2a"     # Primary buttons
    BTN_SECONDARY = "#333333"   # Secondary buttons
    BTN_TERTIARY = "#3a3a3a"    # Tertiary buttons
    BTN_ACCENT_BLUE = "#3498db" # Blue accent (stores)
    BTN_ACCENT_PURPLE = "#9b59b6" # Purple accent (portals)
    BTN_ACCENT_GREEN = "#27ae60" # Green accent (success)
    BTN_ACCENT_RED = "#e74c3c"  # Red accent (errors)
    
    # Typography
    FONT_FAMILY = "SF Pro Display"
    FONT_SIZE_XL = 28           # Main titles
    FONT_SIZE_L = 22            # Section titles
    FONT_SIZE_M = 14            # Headings
    FONT_SIZE_S = 12            # Body text
    FONT_SIZE_XS = 11           # Small text
    FONT_SIZE_CODE = 10         # Code/monospace
    
    # Spacing
    PADDING_XL = 40             # Extra large padding
    PADDING_L = 30              # Large padding
    PADDING_M = 20              # Medium padding
    PADDING_S = 16              # Small padding
    PADDING_XS = 8              # Extra small padding
    
    # Border radius
    RADIUS_L = 12               # Large radius (main frames)
    RADIUS_M = 8                # Medium radius (buttons, inputs)
    RADIUS_S = 6                # Small radius (small elements)
    RADIUS_XS = 4               # Extra small radius

def adjust_brightness(hex_color, adjustment):
    """Adjust brightness of a hex color."""
    hex_color = hex_color.lstrip('#')
    r = max(0, min(255, int(hex_color[0:2], 16) + adjustment))
    g = max(0, min(255, int(hex_color[2:4], 16) + adjustment))
    b = max(0, min(255, int(hex_color[4:6], 16) + adjustment))
    return f"#{r:02x}{g:02x}{b:02x}"

# Helper functions for common UI elements
def create_button(parent, text, command, color=Style.BTN_SECONDARY, height=36, font_size=11):
    """Create a consistently styled button."""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        font=(Style.FONT_FAMILY, font_size),
        corner_radius=Style.RADIUS_S,
        height=height,
        border_width=0,
        fg_color=color,
        hover_color=adjust_brightness(color, 40),
        text_color=Style.TEXT_PRIMARY
    )

def create_entry(parent, placeholder="", width=300, height=36):
    """Create a consistently styled entry field."""
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        font=(Style.FONT_FAMILY, Style.FONT_SIZE_XS),
        corner_radius=Style.RADIUS_S,
        width=width,
        height=height,
        fg_color=Style.BG_TERTIARY,
        border_color=Style.BORDER_MEDIUM,
        text_color=Style.TEXT_PRIMARY
    )

def create_frame(parent, fg_color=Style.BG_SECONDARY, border=True):
    """Create a consistently styled frame."""
    return ctk.CTkFrame(
        parent,
        corner_radius=Style.RADIUS_M,
        fg_color=fg_color,
        border_width=1 if border else 0,
        border_color=Style.BORDER_LIGHT if border else None
    )