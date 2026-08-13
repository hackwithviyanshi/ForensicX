from metadata import get_file_metadata


file_path = "test_evidence.txt"

metadata = get_file_metadata(file_path)

print("File Name:", metadata["file_name"])
print("File Type:", metadata["file_type"])
print("File Size:", metadata["file_size"], "KB")
print("Created:", metadata["created"])
print("Modified:", metadata["modified"])
print("Accessed:", metadata["accessed"])