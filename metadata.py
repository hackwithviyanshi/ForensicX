import os
from datetime import datetime


def get_file_metadata(file_path):

    file_name = os.path.basename(file_path)

    file_extension = os.path.splitext(file_name)[1]

    if file_extension:
        file_type = file_extension.replace(".", "").upper()
    else:
        file_type = "Unknown"

    file_size_bytes = os.path.getsize(file_path)

    file_size_kb = file_size_bytes / 1024

    created_time = datetime.fromtimestamp(
        os.path.getctime(file_path)
    )

    modified_time = datetime.fromtimestamp(
        os.path.getmtime(file_path)
    )

    accessed_time = datetime.fromtimestamp(
        os.path.getatime(file_path)
    )

    return {
        "file_name": file_name,
        "file_type": file_type,
        "file_size": file_size_kb,
        "created": created_time,
        "modified": modified_time,
        "accessed": accessed_time
    }