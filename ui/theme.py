ACCENT = "#7C3AED"
ACCENT_BRIGHT = "#9D5CFF"
ACCENT_DIM = "#4C1D95"
BG_DEEP = "#0A0A0F"
BG_BASE = "#0F0F17"
BG_SURFACE = "#14141E"
BG_CARD = "#1A1A26"
BG_HOVER = "#22223A"
BG_SELECTED = "#1E1B33"
BORDER = "#2A2A3E"
BORDER_ACCENT = "#3D2E6B"
TEXT_PRIMARY = "#EEEEF5"
TEXT_SECONDARY = "#8888AA"
TEXT_DIM = "#55556A"


STYLESHEET = f"""
QWidget {{
    background-color: {BG_BASE};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", "SF Pro Display", sans-serif;
    font-size: 13px;
    border: none;
    outline: none;
}}

QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background: {BG_DEEP};
    width: 6px;
    margin: 0;
    border-radius: 3px;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_ACCENT};
    border-radius: 3px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    height: 0px;
}}

QLineEdit {{
    background: {BG_SURFACE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    selection-background-color: {ACCENT_DIM};
}}

QLineEdit:focus {{
    border-color: {ACCENT};
    background: {BG_CARD};
}}

QLineEdit::placeholder {{
    color: {TEXT_DIM};
}}

QPushButton {{
    background: {BG_SURFACE};
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    color: {TEXT_SECONDARY};
    font-size: 13px;
    font-weight: 500;
}}

QPushButton:hover {{
    background: {BG_HOVER};
    border-color: {BORDER_ACCENT};
    color: {TEXT_PRIMARY};
}}

QPushButton:pressed {{
    background: {BG_SELECTED};
    border-color: {ACCENT};
}}

QPushButton#accent {{
    background: {ACCENT};
    border-color: {ACCENT};
    color: white;
    font-weight: 600;
}}

QPushButton#accent:hover {{
    background: {ACCENT_BRIGHT};
    border-color: {ACCENT_BRIGHT};
}}

QPushButton#accent:pressed {{
    background: {ACCENT_DIM};
}}

QPushButton#danger {{
    background: transparent;
    border: 1.5px solid #7F1D1D;
    color: #F87171;
}}

QPushButton#danger:hover {{
    background: #2D0A0A;
    border-color: #EF4444;
    color: #FCA5A5;
}}

QDialog {{
    background: {BG_SURFACE};
    border: 1.5px solid {BORDER_ACCENT};
    border-radius: 14px;
}}

QLabel {{
    background: transparent;
    color: {TEXT_PRIMARY};
}}

QLabel#secondary {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
}}

QMenu {{
    background: {BG_CARD};
    border: 1.5px solid {BORDER_ACCENT};
    border-radius: 10px;
    padding: 5px;
}}

QMenu::item {{
    padding: 8px 16px;
    border-radius: 6px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
}}

QMenu::item:selected {{
    background: {BG_HOVER};
    color: {TEXT_PRIMARY};
}}

QMenu::separator {{
    height: 1px;
    background: {BORDER};
    margin: 4px 10px;
}}
"""
