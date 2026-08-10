import customtkinter as ctk
import sqlite3
from tkinter import filedialog
import hashlib

# =========================
# DATABASE
# =========================

def initialize_database():
    connection = sqlite3.connect("forensicx.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_name TEXT NOT NULL,
            investigator TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# =========================
# CREATE CASE
# =========================

def create_case():
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
        case_name = case_name_entry.get()
        investigator = investigator_entry.get()

        connection = sqlite3.connect("forensicx.db")
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


# =========================
# DASHBOARD
# =========================

def show_dashboard():

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

    # Active Cases Card
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

    connection = sqlite3.connect("forensicx.db")
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

    # Evidence Card
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

    evidence_count = ctk.CTkLabel(
        evidence_card,
        text="0",
        font=("Arial", 28, "bold")
    )

    evidence_count.pack()

    # Create Case Button
    new_case_button = ctk.CTkButton(
        main_area,
        text="+  Create New Case",
        width=220,
        height=45,
        command=create_case
    )

    new_case_button.pack(
        anchor="w",
        padx=40,
        pady=(25, 10)
    )


# =========================
# CASES PAGE
# =========================

def show_cases():

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

    connection = sqlite3.connect("forensicx.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, case_name, investigator, created_at FROM cases"
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

        return

    for case in cases:

        case_id, case_name, investigator, created_at = case

        case_label = ctk.CTkLabel(
            main_area,
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
            padx=40,
            pady=8
        )

# =========================
# CASES PAGE
# =========================
def show_evidence():
    for widget in main_area.winfo_children():
        widget.destroy()

    evidence_title = ctk.CTkLabel(
        main_area,
        text="Evidence",
        font=("Arial", 30, "bold")
    )

    evidence_title.pack(
        anchor="w",
        padx=40,
        pady=(40, 20)
    )

    selected_file_label = ctk.CTkLabel(
        main_area,
        text="No file selected",
        font=("Arial", 15)
    )

    selected_file_label.pack(
        anchor="w",
        padx=40,
        pady=20
    )
    hash_label = ctk.CTkLabel(
        main_area,
        text="SHA-256: Not calculated",
        font=("Arial", 14)
    )

    hash_label.pack(
        anchor="w",
        padx=40,
        pady=10
    )

    def calculate_hash(file_path):
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select Evidence File"
        )
        file_hash = calculate_hash(file_path)

        hash_label.configure(
            text=f"SHA-256:\n{file_hash}"
        )

        if file_path:
            selected_file_label.configure(
                text=f"Selected File:\n{file_path}"
            )

    select_file_button = ctk.CTkButton(
        main_area,
        text="Select Evidence File",
        width=220,
        height=45,
        command=select_file
    )

    select_file_button.pack(
        anchor="w",
        padx=40,
        pady=10
    )
# =========================
# APPLICATION WINDOW
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


# ForensicX Logo
logo_label = ctk.CTkLabel(
    sidebar,
    text="FORENSICX",
    font=("Arial", 22, "bold")
)

logo_label.pack(pady=30)


# Dashboard Button
dashboard_button = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    width=200,
    height=40,
    command=show_dashboard
)

dashboard_button.pack(pady=10)


# Cases Button
cases_button = ctk.CTkButton(
    sidebar,
    text="Cases",
    width=200,
    height=40,
    command=show_cases
)

cases_button.pack(pady=10)
#Evidence button
evidence_button = ctk.CTkButton(
    sidebar,
    text="Evidence",
    width=200,
    height=40,
    command=show_evidence
)

evidence_button.pack(pady=10)

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
# START APPLICATION
# =========================

initialize_database()

show_dashboard()

app.mainloop()