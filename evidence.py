import os
import customtkinter as ctk
from tkinter import filedialog

from hashing import calculate_sha256


def show_evidence(main_area):

    # Clear main area
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

    def select_file():

        file_path = filedialog.askopenfilename(
            title="Select Evidence File"
        )

        # User cancelled
        if not file_path:
            return

        file_hash = calculate_sha256(file_path)

        file_name = os.path.basename(file_path)

        selected_file_label.configure(
            text=f"Selected File:\n{file_name}"
        )

        hash_label.configure(
            text=f"SHA-256:\n{file_hash}"
        )

        print("Evidence file:", file_path)
        print("SHA-256:", file_hash)

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