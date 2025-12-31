from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS

# Test truncation
def main():
    result = get_file_content("calculator", "lorem.txt")

    print("Length:", len(result))
    print("Ends with truncation notice:", result.endswith(f'[...File "lorem.txt" truncated at {MAX_FILE_CHARS} characters]'))

    print()

    # Other test cases
    print("main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("/bin/cat (should error):")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("pkg/does_not_exist.py (should error):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()