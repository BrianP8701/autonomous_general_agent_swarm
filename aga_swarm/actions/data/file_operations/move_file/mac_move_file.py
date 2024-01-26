import shutil
from pydantic import validate_arguments

# Function to move a file on a mac
@validate_arguments
def mac_move_file(file_path: str, new_file_path: str) -> dict:
    try:
        # Move the file
        shutil.move(file_path, new_file_path)
        return {'status_message': 'Success', 'error_message': ''}
    except Exception as e:
        # Return the error message if an exception occurs
        return {'status_message': 'Failure', 'error_message': str(e)}

# Main section
@validate_arguments
def main(file_path: str, new_file_path: str) -> dict:
    return mac_move_file(file_path, new_file_path)