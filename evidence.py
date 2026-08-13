import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from database import get_connection
from hashing import calculate_sha256
from metadata import get_file_metadata

def show_evidence(main_area):

    # =========================
    # CLEAR MAIN AREA
    # =========================

    for widget in main_area.winfo_children():
        widget.destroy()

    # =========================
    # TITLE
    # =========================

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

    # =========================
    # ADD EVIDENCE SECTION
    # =========================

    add_frame = ctk.CTkFrame(main_area)

    add_frame.pack(
        fill="x",
        padx=40,
        pady=10
    )

    add_title = ctk.CTkLabel(
        add_frame,
        text="Add Evidence",
        font=("Arial", 20, "bold")
    )

    add_title.pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    # =========================
    # GET CASES
    # =========================

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, case_name
        FROM cases
        ORDER BY id DESC
        """
    )

    cases = cursor.fetchall()

    connection.close()

    if not cases:

        no_cases_label = ctk.CTkLabel(
            add_frame,
            text="No cases available. Create a case first.",
            font=("Arial", 15)
        )

        no_cases_label.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        return

    # =========================
    # CASE SELECTION
    # =========================

    case_label = ctk.CTkLabel(
        add_frame,
        text="Select Case",
        font=("Arial", 14, "bold")
    )

    case_label.pack(
        anchor="w",
        padx=20,
        pady=(5, 5)
    )

    case_options = [
        f"Case #{case_id} - {case_name}"
        for case_id, case_name in cases
    ]

    case_dropdown = ctk.CTkComboBox(
        add_frame,
        values=case_options,
        width=400
    )

    case_dropdown.pack(
        anchor="w",
        padx=20,
        pady=5
    )

    case_dropdown.set(case_options[0])

    # =========================
    # FILE INFORMATION
    # =========================

    selected_file_label = ctk.CTkLabel(
        add_frame,
        text="No file selected",
        font=("Arial", 14)
    )

    selected_file_label.pack(
        anchor="w",
        padx=20,
        pady=15
    )

    hash_label = ctk.CTkLabel(
        add_frame,
        text="SHA-256: Not calculated",
        font=("Arial", 12)
    )

    hash_label.pack(
        anchor="w",
        padx=20,
        pady=5
    )
    metadata_label = ctk.CTkLabel(
        add_frame,
        text="File Metadata: Not available",
        font=("Arial", 12),
        justify="left"
    )

    metadata_label.pack(
        anchor="w",
        padx=20,
        pady=10
    )

    selected_file = {
        "path": None,
        "hash": None
    }

    # =========================
    # SELECT FILE
    # =========================

    def select_file():

        file_path = filedialog.askopenfilename(
            title="Select Evidence File"
        )

        if not file_path:
            return

        file_hash = calculate_sha256(file_path)
        file_metadata = get_file_metadata(file_path)

        selected_file["path"] = file_path
        selected_file["hash"] = file_hash

        file_name = os.path.basename(file_path)

        selected_file_label.configure(
            text=f"Selected File: {file_name}"
        )

        hash_label.configure(
            text=f"SHA-256: {file_hash}"
        )
        metadata_label.configure(
            text="File Metadata: Not available"
        )
        metadata_label.configure(
            text=(
            f"File Type: {file_metadata['file_type']}\n"
            f"File Size: {file_metadata['file_size']:.2f} KB\n"
            f"Created: {file_metadata['created']}\n"
            f"Modified: {file_metadata['modified']}\n"
            f"Accessed: {file_metadata['accessed']}"
            )
)

    select_file_button = ctk.CTkButton(
        add_frame,
        text="Select Evidence File",
        width=220,
        height=40,
        command=select_file
    )

    select_file_button.pack(
        anchor="w",
        padx=20,
        pady=10
    )

    # =========================
    # SAVE EVIDENCE
    # =========================

    def save_evidence():

        if not selected_file["path"]:
            messagebox.showwarning(
                "No Evidence",
                "Please select an evidence file first."
            )
            return

        selected_case = case_dropdown.get()

        case_id = int(
            selected_case.split("#")[1].split(" ")[0]
        )

        file_name = os.path.basename(
            selected_file["path"]
        )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO evidence
            (case_id, file_name, file_path, sha256)
            VALUES (?, ?, ?, ?)
            """,
            (
                case_id,
                file_name,
                selected_file["path"],
                selected_file["hash"]
            )
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Evidence Saved",
            "Evidence has been successfully added."
        )

        selected_file["path"] = None
        selected_file["hash"] = None

        selected_file_label.configure(
            text="No file selected"
        )

        hash_label.configure(
            text="SHA-256: Not calculated"
        )

        load_evidence_records()

    save_button = ctk.CTkButton(
        add_frame,
        text="Save Evidence",
        width=220,
        height=40,
        command=save_evidence
    )

    save_button.pack(
        anchor="w",
        padx=20,
        pady=(10, 20)
    )

    # =========================
    # SAVED RECORDS TITLE
    # =========================

    records_title = ctk.CTkLabel(
        main_area,
        text="Evidence Records",
        font=("Arial", 22, "bold")
    )

    records_title.pack(
        anchor="w",
        padx=40,
        pady=(25, 10)
    )

    records_frame = ctk.CTkScrollableFrame(
        main_area,
        height=250
    )

    records_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(0, 20)
    )

    # =========================
    # VERIFY INTEGRITY
    # =========================

    def verify_integrity(evidence_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT file_path, sha256
            FROM evidence
            WHERE id = ?
            """,
            (evidence_id,)
        )

        result = cursor.fetchone()

        connection.close()

        if not result:
            messagebox.showerror(
                "Error",
                "Evidence record not found."
            )
            return

        file_path, original_hash = result

        if not os.path.exists(file_path):

            messagebox.showerror(
                "File Not Found",
                "The original evidence file could not be found."
            )

            return

        current_hash = calculate_sha256(file_path)

        if original_hash == current_hash:

            messagebox.showinfo(
                "Integrity Verified",
                "SHA-256 hash matches the original hash.\n\n"
                "Evidence integrity verified."
            )

        else:

            messagebox.showwarning(
                "Hash Mismatch",
                "The current SHA-256 does not match the original hash.\n\n"
                "The file may have been modified."
            )

    # =========================
    # LOAD EVIDENCE RECORDS
    # =========================

    def load_evidence_records():

        for widget in records_frame.winfo_children():
            widget.destroy()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                evidence.id,
                evidence.file_name,
                evidence.sha256,
                evidence.added_at,
                cases.case_name
            FROM evidence
            LEFT JOIN cases
            ON evidence.case_id = cases.id
            ORDER BY evidence.id DESC
            """
        )

        records = cursor.fetchall()

        connection.close()

        if not records:

            no_records = ctk.CTkLabel(
                records_frame,
                text="No evidence records found.",
                font=("Arial", 14)
            )

            no_records.pack(
                anchor="w",
                padx=15,
                pady=15
            )

            return

        for record in records:

            evidence_id, file_name, sha256, added_at, case_name = record

            record_frame = ctk.CTkFrame(
                records_frame
            )

            record_frame.pack(
                fill="x",
                pady=6
            )

            record_text = (
                f"Evidence #{evidence_id}\n"
                f"File: {file_name}\n"
                f"Case: {case_name}\n"
                f"SHA-256: {sha256}\n"
                f"Added: {added_at}"
            )

            record_label = ctk.CTkLabel(
                record_frame,
                text=record_text,
                justify="left",
                font=("Arial", 13)
            )

            record_label.pack(
                anchor="w",
                padx=15,
                pady=12
            )

            verify_button = ctk.CTkButton(
                record_frame,
                text="Verify Integrity",
                width=150,
                height=35,
                command=lambda eid=evidence_id:
                    verify_integrity(eid)
            )

            verify_button.pack(
                anchor="w",
                padx=15,
                pady=(0, 12)
            )

    # Load records when page opens
    load_evidence_records()