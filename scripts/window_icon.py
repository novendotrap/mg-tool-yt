import os
from tkinter import PhotoImage

def apply_window_icon(window):
    """Apply the app icon to a Tk or Toplevel `window`.

    Looks for `images/ico.ico`, `images/ico.jpg`, `ico.ico`, `ico.jpg`.
    Quietly returns if no icon is found or loading fails.
    """
    icon_paths = [
        "images/ico.ico",
        "images/ico.jpg",
        "ico.ico",
        "ico.jpg",
    ]

    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            try:
                if icon_path.lower().endswith('.ico'):
                    try:
                        window.iconbitmap(icon_path)
                        # Keep a marker that an ico was applied
                        window._icon_path = icon_path
                        return
                    except Exception:
                        # Some platforms may not support iconbitmap for certain windows
                        pass
                else:
                    try:
                        img = PhotoImage(file=icon_path)
                        # Primary method
                        try:
                            window.iconphoto(True, img)
                        except Exception:
                            pass
                        # Fallback / alternate API
                        try:
                            window.wm_iconphoto(False, img)
                        except Exception:
                            pass
                        # Keep a reference to avoid garbage collection which clears the icon
                        try:
                            window._icon_image = img
                        except Exception:
                            pass
                        window._icon_path = icon_path
                        return
                    except Exception:
                        pass
            except Exception:
                continue
    return
