import requests
import json
import os
from tkinter import Tk, filedialog


def get_file_path():
    """
    Opens a file selection dialog and returns the selected file path.
    """
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()
    root.destroy() # Close the main window
    return file_path


def validate_json_file(file_path):
    """
    Checks if the selected file is a JSON file. If it is, return the file path,
    otherwise, raise a ValueError.
    """
    if not file_path:  # Checks if the file path is not empty
        raise ValueError("No file selected.")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".json":
        return file_path
    else:
        raise ValueError("Unsupported file type. Please select a JSON file.")


try:
    file_path = get_file_path()
    valid_json_path = validate_json_file(file_path)
    print(f"File validated: {valid_json_path}")

    json_data = open(valid_json_path).read()

    # Convert the JSON string into a Python dictionary
    data = json.loads(json_data)

    # List to keep track of entries with 404 status
    broken_links = []

    # Loop through each link in the JSON
    for link in data['links']:
        try:
            # Check the status code of the URL
            response = requests.get(link['url'], allow_redirects=True, timeout=10)
            if response.status_code == 404:
                # If 404, add to the broken_links list
                print(f"Broken link: {link['url']}")
                broken_links.append(link)
        except requests.ConnectionError as e:
            print(f"Connection error while checking URL {link['url']}. Treating as 404. ERROR: {e}")
            broken_links.append(link)
        except requests.Timeout as e:
            print(f"Timeout for URL {link['url']}. Treating as 404. ERROR: {e}")
            broken_links.append(link)
        except requests.RequestException as e:
            print(f"Error while checking URL {link['url']}: {e}")

    # Print or save the broken links as needed
    with open('broken_links.json', 'w') as f:
        if(len(broken_links) > 0):
            f.write(json.dumps(broken_links, indent=4))
    # print(json.dumps(broken_links, indent=4))
except ValueError as e:
    print(e)
