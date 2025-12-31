#!/usr/bin/env python3

import os
from config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            raise ValueError(
                f'Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_path):
            raise ValueError(
                f'File not found or is not a regular file: "{file_path}"'
            )

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"
