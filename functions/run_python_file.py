import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        # Resolve working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Resolve the target file path safely
        target_path_abs  = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Prevent directory traversal
        if os.path.commonpath([working_dir_abs, target_path_abs ]) != working_dir_abs:
            raise ValueError(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        # Must exist and be a regular file
        if not os.path.isfile(target_path_abs ):
            raise ValueError(
                f'Error: "{file_path}" does not exist or is not a regular file'
            )

        # Must be a Python file
        if not target_path_abs .endswith(".py"):
            raise ValueError(
                f'Error: "{file_path}" is not a Python file'
            )

        # Build command
        command = ["python", target_path_abs ]

        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        # Non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # No output at all
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append("STDOUT:\n" + result.stdout)
            if result.stderr:
                output_parts.append("STDERR:\n" + result.stderr)

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = {
    "name": "run_python_file",
    "description": "Executes a Python file inside the working directory with optional command line arguments",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the Python file to run, relative to the working directory"
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Optional command line arguments passed to the Python file"
            }
        },
        "required": ["file_path"]
    }
}