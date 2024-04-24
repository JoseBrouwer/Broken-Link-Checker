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


def check_url(url):
    # Start a session and disable automatic redirection handling
    with requests.Session() as session:
        session.max_redirects = 10  # Safeguard against infinite redirects
        try:
            response = session.get(url, allow_redirects=False, timeout=10)

            # Check if initial response is a 404
            if response.status_code == 404:
                print(f"Initial 404 detected at {url}")

                # Manually handle redirects if 404 is detected initially
                while response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.headers["Location"]
                    print(f"Redirecting to {redirect_url}")
                    response = session.get(
                        redirect_url, allow_redirects=False, timeout=10
                    )

                # Final URL status check
                if response.status_code == 200:
                    print(f"Successfully redirected to {response.url} with status 200")
                    return False
                else:
                    print(f"Ended with status {response.status_code} at {response.url}")
                    return True
            else:
                print(f"Initial status code {response.status_code} at {url}")
                return False

        except requests.Timeout:
            print("Timeout occurred while checking URL")
            return True
        except requests.TooManyRedirects:
            print("Too many redirects")
            return True
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return True


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
        if(check_url(link['url'])):
            broken_links.append(link)     

    # Print or save the broken links as needed
    with open('broken_links.json', 'w') as f:
        if(len(broken_links) > 0):
            f.write(json.dumps(broken_links, indent=4))
except ValueError as e:
    print(e)
