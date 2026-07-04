import os

def create_or_write_file(filepath: str, content: str):
    """Creates a new file or completely overwrites an existing one."""
    # Using 'w' (write) mode. It handles any special characters cleanly.
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f" Successfully created/overwrote: {filepath}")

def append_to_file(filepath: str, content: str):
    """Appends text to the end of an existing file without wiping it."""
    # Using 'a' (append) mode.
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f" Successfully updated: {filepath}")

def read_file(filepath: str) -> str:
    """Reads the contents of a file securely."""
    if not os.path.exists(filepath):
        return "Error: File does not exist."
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def delete_file(filepath: str):
    """Deletes a file from the disk safely."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"🗑️ Successfully deleted: {filepath}")
    else:
        print("Error: File not found to delete.")


Available_Tools = {
    "create_or_write_file": {
        "fn": create_or_write_file,
        "description": "Creates a new file or completely overwrites an existing one. Takes two inputs: filepath and content."
    },
    "append_to_file": {
        "fn": append_to_file,
        "description": "Appends text to the end of an existing file without wiping it. Takes two inputs: filepath and content."
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads the contents of a file securely. Takes one input: filepath."
    },
    "delete_file": {
        "fn": delete_file,
        "description": "Deletes a file from the disk safely. Takes one input: filepath."
    },
}


print (f"""{'\n'.join([f"- {name}: {info['description']}" for name, info in Available_Tools.items()])}""")