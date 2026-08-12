import sqlite3
import customtkinter as ctk

from database import get_connection


def create_case(app):

    case_window = ctk.CTkToplevel(app)

    case_window.title("Create New Case")
    case_window.geometry("500x400")

    case_title = ctk.CTkLabel(
        case_window,
        text="Create New Case",
        font=("Arial", 24, "bold")
    )

    case_title.pack(pady=30)

    case_name_entry = ctk.CTkEntry(
        case_window,
        placeholder_text="Enter case name",
        width=300
    )

    case_name_entry.pack(pady=10)

    investigator_entry = ctk.CTkEntry(
        case_window,
        placeholder_text="Enter investigator name",
        width=300
    )

    investigator_entry.pack(pady=10)

    def save_case():

        case_name = case_name_entry.get().strip()
        investigator = investigator_entry.get().strip()

        if not case_name or not investigator:
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO cases (case_name, investigator)
            VALUES (?, ?)
            """,
            (case_name, investigator)
        )

        connection.commit()
        connection.close()

        print("Case saved successfully!")

        case_window.destroy()

    save_button = ctk.CTkButton(
        case_window,
        text="Save Case",
        width=200,
        height=40,
        command=save_case
    )

    save_button.pack(pady=25)


def show_cases(main_area, app):

    # Clear main area
    for widget in main_area.winfo_children():
        widget.destroy()

    cases_title = ctk.CTkLabel(
        main_area,
        text="Cases",
        font=("Arial", 30, "bold")
    )

    cases_title.pack(
        anchor="w",
        padx=40,
        pady=(40, 20)
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, case_name, investigator, created_at
        FROM cases
        ORDER BY id DESC
        """
    )

    cases = cursor.fetchall()

    connection.close()

    if not cases:

        no_cases_label = ctk.CTkLabel(
            main_area,
            text="No cases found.",
            font=("Arial", 16)
        )

        no_cases_label.pack(
            anchor="w",
            padx=40,
            pady=20
        )

    else:

        for case in cases:

            case_id, case_name, investigator, created_at = case

            case_frame = ctk.CTkFrame(
                main_area
            )

            case_frame.pack(
                fill="x",
                padx=40,
                pady=8
            )

            case_label = ctk.CTkLabel(
                case_frame,
                text=(
                    f"Case #{case_id}   |   "
                    f"{case_name}   |   "
                    f"{investigator}   |   "
                    f"{created_at}"
                ),
                font=("Arial", 14)
            )

            case_label.pack(
                anchor="w",
                padx=15,
                pady=12
            )

    new_case_button = ctk.CTkButton(
        main_area,
        text="+  Create New Case",
        width=220,
        height=45,
        command=lambda: create_case(app)
    )

    new_case_button.pack(
        anchor="w",
        padx=40,
        pady=20
    )