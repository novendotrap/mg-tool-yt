import customtkinter as ctk
try:
    from styles.styles import Style, adjust_brightness
except ImportError:
    # Fallback si styles.py no existe
    class Style:
        BG_PRIMARY = "#000000"
        BG_SECONDARY = "#111111"
        BG_TERTIARY = "#1a1a1a"
        BORDER_LIGHT = "#222222"
        BORDER_MEDIUM = "#333333"
        TEXT_PRIMARY = "#e0e0e0"
        TEXT_SECONDARY = "#888888"
        FONT_FAMILY = "SF Pro Display"
    
    def adjust_brightness(hex_color, adjustment):
        hex_color = hex_color.lstrip('#')
        r = max(0, min(255, int(hex_color[0:2], 16) + adjustment))
        g = max(0, min(255, int(hex_color[2:4], 16) + adjustment))
        b = max(0, min(255, int(hex_color[4:6], 16) + adjustment))
        return f"#{r:02x}{g:02x}{b:02x}"

# Ensure a reusable modal creator exists at module level so other modules can import it
def create_modal(parent, title, width, height):
    """Create a CTkToplevel modal with consistent style, icon applied and centered.

    This function is safe to call whether `styles.styles` was imported or the fallback
    is used: it relies on the `Style` symbol defined above in either branch.
    """
    top = ctk.CTkToplevel(parent)
    try:
        from scripts.window_icon import apply_window_icon
        apply_window_icon(top)
        try:
            top.after(150, lambda: apply_window_icon(top))
            top.after(600, lambda: apply_window_icon(top))
        except Exception:
            pass
    except Exception:
        pass
    try:
        top.transient(parent)
    except Exception:
        pass
    top.title(title)
    top.geometry(f"{width}x{height}")
    top.resizable(False, False)
    try:
        top.configure(fg_color=Style.BG_PRIMARY)
    except Exception:
        pass

    # Center dialog
    top.update_idletasks()
    x = (top.winfo_screenwidth() // 2) - (width // 2)
    y = (top.winfo_screenheight() // 2) - (height // 2)
    try:
        top.geometry(f'{width}x{height}+{x}+{y}')
    except Exception:
        pass

    return top

    def create_modal(parent, title, width, height):
        """Create a CTkToplevel modal with consistent style, icon applied and centered."""
        top = ctk.CTkToplevel(parent)
        try:
            from scripts.window_icon import apply_window_icon
            apply_window_icon(top)
            try:
                top.after(150, lambda: apply_window_icon(top))
                top.after(600, lambda: apply_window_icon(top))
            except Exception:
                pass
        except Exception:
            pass
        try:
            top.transient(parent)
        except Exception:
            pass
        top.title(title)
        top.geometry(f"{width}x{height}")
        top.resizable(False, False)
        top.configure(fg_color=Style.BG_PRIMARY)

        # Center dialog
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (width // 2)
        y = (top.winfo_screenheight() // 2) - (height // 2)
        try:
            top.geometry(f'{width}x{height}+{x}+{y}')
        except Exception:
            pass

        return top

def ask_integer(parent, title, prompt, initialvalue=1, minvalue=1):
    """Show a modal integer prompt with dark minimalist style. Returns int or None."""
    result = {'value': None}
    top = create_modal(parent, title, 340, 160)

    frame = ctk.CTkFrame(
        top, 
        corner_radius=8,
        fg_color=Style.BG_SECONDARY,
        border_width=1,
        border_color=Style.BORDER_LIGHT
    )
    frame.pack(expand=True, fill='both', padx=20, pady=20)

    label = ctk.CTkLabel(
        frame, 
        text=prompt, 
        anchor='w',
        font=(Style.FONT_FAMILY, 12),
        text_color=Style.TEXT_PRIMARY
    )
    label.pack(fill='x', pady=(12, 8), padx=16)

    entry_var = ctk.StringVar(value=str(initialvalue))
    entry = ctk.CTkEntry(
        frame, 
        textvariable=entry_var,
        font=(Style.FONT_FAMILY, 11),
        corner_radius=6,
        fg_color=Style.BG_TERTIARY,
        border_color=Style.BORDER_MEDIUM,
        text_color=Style.TEXT_PRIMARY,
        height=36
    )
    entry.pack(fill='x', pady=(0, 12), padx=16)

    btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
    btn_frame.pack(fill='x', padx=16, pady=(0, 8))

    def on_ok(event=None):
        v = entry_var.get().strip()
        try:
            n = int(v)
            if n < minvalue:
                return
            result['value'] = n
            top.destroy()
        except Exception:
            return

    def on_cancel():
        result['value'] = None
        top.destroy()

    ok_btn = ctk.CTkButton(
        btn_frame, 
        text='OK', 
        width=80,
        font=(Style.FONT_FAMILY, 11),
        fg_color=Style.BTN_SECONDARY,
        text_color=Style.TEXT_PRIMARY,
        corner_radius=6,
        height=32,
        hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
        command=on_ok
    )
    ok_btn.pack(side='right', padx=(8, 0))
    
    cancel_btn = ctk.CTkButton(
        btn_frame, 
        text='Cancel', 
        width=80,
        font=(Style.FONT_FAMILY, 11),
        fg_color=Style.BTN_TERTIARY,
        text_color=Style.TEXT_PRIMARY,
        corner_radius=6,
        height=32,
        hover_color=adjust_brightness(Style.BTN_TERTIARY, 40),
        command=on_cancel
    )
    cancel_btn.pack(side='right')

    entry.bind('<Return>', on_ok)
    entry.focus_set()
    entry.select_range(0, 'end')

    # Modal behavior
    try:
        top.grab_set()
        parent.wait_window(top)
    except Exception:
        top.wait_window()

    return result['value']

def ask_text(parent, title, prompt, initialvalue=''):
    """Show a modal text prompt with dark minimalist style. Returns str or None."""
    result = {'value': None}
    top = create_modal(parent, title, 440, 180)

    frame = ctk.CTkFrame(
        top, 
        corner_radius=8,
        fg_color=Style.BG_SECONDARY,
        border_width=1,
        border_color=Style.BORDER_LIGHT
    )
    frame.pack(expand=True, fill='both', padx=20, pady=20)

    label = ctk.CTkLabel(
        frame, 
        text=prompt, 
        anchor='w',
        font=(Style.FONT_FAMILY, 12),
        text_color=Style.TEXT_PRIMARY
    )
    label.pack(fill='x', pady=(12, 8), padx=16)

    entry_var = ctk.StringVar(value=str(initialvalue))
    entry = ctk.CTkEntry(
        frame, 
        textvariable=entry_var,
        font=(Style.FONT_FAMILY, 11),
        corner_radius=6,
        fg_color=Style.BG_TERTIARY,
        border_color=Style.BORDER_MEDIUM,
        text_color=Style.TEXT_PRIMARY,
        height=36
    )
    entry.pack(fill='x', pady=(0, 12), padx=16)

    btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
    btn_frame.pack(fill='x', padx=16, pady=(0, 8))

    def on_ok(event=None):
        v = entry_var.get()
        result['value'] = v
        top.destroy()

    def on_cancel():
        result['value'] = None
        top.destroy()

    ok_btn = ctk.CTkButton(
        btn_frame, 
        text='OK', 
        width=80,
        font=(Style.FONT_FAMILY, 11),
        fg_color=Style.BTN_SECONDARY,
        text_color=Style.TEXT_PRIMARY,
        corner_radius=6,
        height=32,
        hover_color=adjust_brightness(Style.BTN_SECONDARY, 40),
        command=on_ok
    )
    ok_btn.pack(side='right', padx=(8, 0))
    
    cancel_btn = ctk.CTkButton(
        btn_frame, 
        text='Cancel', 
        width=80,
        font=(Style.FONT_FAMILY, 11),
        fg_color=Style.BTN_TERTIARY,
        text_color=Style.TEXT_PRIMARY,
        corner_radius=6,
        height=32,
        hover_color=adjust_brightness(Style.BTN_TERTIARY, 40),
        command=on_cancel
    )
    cancel_btn.pack(side='right')

    entry.bind('<Return>', on_ok)
    entry.focus_set()
    entry.select_range(0, 'end')

    # Modal behavior
    try:
        top.grab_set()
        parent.wait_window(top)
    except Exception:
        top.wait_window()

    return result['value']