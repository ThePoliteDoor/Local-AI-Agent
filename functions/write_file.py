import os

def write_file(working_directory, file_path, content):
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        # Security check: must be inside working directory
        if os.path.commonpath([working_dir_abs, target_path_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Cannot write to a directory
        if os.path.isdir(target_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure parent directories exist
        parent_dir = os.path.dirname(target_path_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the file
        with open(target_path_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = {
    "name": "write_file",
    "description": "Writes or overwrites a file inside the working directory with the provided content",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write, relative to the working directory"
            },
            "content": {
                "type": "string",
                "description": "The text content to write into the file"
            }
        },
        "required": ["file_path", "content"]
    }
}