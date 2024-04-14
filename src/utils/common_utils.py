# common_utils.py
import re
import string

# Constants for operations
FILENAME_VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
GIT_DIFF_FILENAME_REGEX_PATTERN = r"\+\+\+ b/(.*)"

def validate_filename(filename: str) -> bool:
    """
    Validates a filename to ensure it does not contain disallowed characters
    and does not traverse directories.
    """
    return ".." not in filename and "/" not in filename and all(
        char in FILENAME_VALID_CHARS for char in filename
    )

def extract_filenames_from_diff_text(diff_text: str):
    """
    Extracts filenames from git diff output using a regular expression.
    Returns a list of valid filenames.
    """
    filenames = re.findall(GIT_DIFF_FILENAME_REGEX_PATTERN, diff_text)
    return [fn for fn in filenames if validate_filename(fn)]

def format_file_contents_as_markdown(filenames):
    """
    Formats the contents of files listed in filenames as Markdown.
    Reads each file, ensuring the file exists and is readable, and formats it.
    """
    formatted_files = ""
    for filename in filenames:
        try:
            with open(filename, "r") as file:
                file_content = file.read()
            formatted_files += f"\n## {filename}\n```python\n{file_content}\n```\n"
        except Exception as e:
            print(f"Could not read file {filename}: {e}")
    return formatted_files
