import customtkinter as ctk

from database import initialize_database
from dashboard import show_dashboard
from cases import show_cases
from evidence import show_evidence


# =========================
# APPLICATION SETTINGS
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()

app.title("ForensicX - Digital Forensics Toolkit")
app.geometry("1000x650")


# =========================
# SIDEBAR
# =========================

sidebar = ctk.CTkFrame(
    app,
    width=240,
    corner_radius=0
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# =========================
# LOGO
# =========================

logo_label = ctk.CTkLabel(
    sidebar,
    text="FORENSICX",
    font=("Arial", 22, "bold")
)

logo_label.pack(pady=30)


# =========================
# MAIN CONTENT AREA
# =========================

main_area = ctk.CTkFrame(
    app,
    corner_radius=0
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================
# NAVIGATION FUNCTIONS
# =========================

def open_dashboard():
    show_dashboard(main_area)


def open_cases():
    show_cases(main_area, app)


def open_evidence():
    show_evidence(main_area)


# =========================
# SIDEBAR BUTTONS
# =========================

dashboard_button = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    width=200,
    height=40,
    command=open_dashboard
)

dashboard_button.pack(pady=10)


cases_button = ctk.CTkButton(
    sidebar,
    text="Cases",
    width=200,
    height=40,
    command=open_cases
)

cases_button.pack(pady=10)


evidence_button = ctk.CTkButton(
    sidebar,
    text="Evidence",
    width=200,
    height=40,
    command=open_evidence
)

evidence_button.pack(pady=10)


# =========================
# START APPLICATION
# =========================

initialize_database()

open_dashboard()

app.mainloop()