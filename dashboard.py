import sqlite3
import customtkinter as ctk

from database import get_connection


def show_dashboard(main_area):

    # Clear main area
    for widget in main_area.winfo_children():
        widget.destroy()

    dashboard_title = ctk.CTkLabel(
        main_area,
        text="Dashboard",
        font=("Arial", 30, "bold")
    )

    dashboard_title.pack(
        anchor="w",
        padx=40,
        pady=(40, 10)
    )

    welcome_label = ctk.CTkLabel(
        main_area,
        text="Welcome to the Digital Forensics Investigation Toolkit",
        font=("Arial", 16)
    )

    welcome_label.pack(
        anchor="w",
        padx=40,
        pady=(0, 30)
    )

    cards_frame = ctk.CTkFrame(
        main_area,
        fg_color="transparent"
    )

    cards_frame.pack(
        anchor="w",
        padx=40,
        pady=10
    )

    # =========================
    # ACTIVE CASES CARD
    # =========================

    cases_card = ctk.CTkFrame(
        cards_frame,
        width=220,
        height=120
    )

    cases_card.pack(
        side="left",
        padx=(0, 15)
    )

    cases_title = ctk.CTkLabel(
        cases_card,
        text="ACTIVE CASES",
        font=("Arial", 14, "bold")
    )

    cases_title.pack(pady=(20, 5))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM cases")

    case_count = cursor.fetchone()[0]

    connection.close()

    cases_count = ctk.CTkLabel(
        cases_card,
        text=str(case_count),
        font=("Arial", 28, "bold")
    )

    cases_count.pack()

    # =========================
    # EVIDENCE CARD
    # =========================

    evidence_card = ctk.CTkFrame(
        cards_frame,
        width=220,
        height=120
    )

    evidence_card.pack(
        side="left",
        padx=15
    )

    evidence_title = ctk.CTkLabel(
        evidence_card,
        text="EVIDENCE FILES",
        font=("Arial", 14, "bold")
    )

    evidence_title.pack(pady=(20, 5))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM evidence")

    evidence_count_value = cursor.fetchone()[0]

    connection.close()

    evidence_count = ctk.CTkLabel(
        evidence_card,
        text=str(evidence_count_value),
        font=("Arial", 28, "bold")
    )

    evidence_count.pack()