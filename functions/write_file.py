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