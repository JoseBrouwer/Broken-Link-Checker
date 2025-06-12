import requests
import json
import re
import os
from tkinter import Tk, filedialog
from urllib.parse import urlparse
from copy import deepcopy


def get_file_path():
    """
    Opens a file selection dialog and returns the selected file path.

    Args: 
        None
    
    Returns: 
        file_path (string): path to file sleected using GUI
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

    Args: 
        file_path (string): file path to the file to validate

    Returns: 
        file_path (string): file path to the validated file
        ValueError: The file was not JSON and an error was raised
    """
    if not file_path:  # Checks if the file path is not empty
        raise ValueError("No file selected.")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".json":
        return file_path
    else:
        raise ValueError("Unsupported file type. Please select a JSON file.")

def record_broken_link(link, url, error, origin_url=None, origin_file=None):
    """
    Appends a broken link entry to broken_links with original file/url context and error details.

    Args:
        link (dict): The link object being checked.
        url (str): The actual URL that failed.
        error (str): The error message or status.
        origin_url (str, optional): The original URL from the source data.
        origin_file (str, optional): The original file from the source data.

    Returns:
        None, appends broken links and their respective information as a dictionary to the broken_links array
    """
    broken = {
        "file": origin_file or link.get("file"),
        "url": origin_url or url,
        "Error": error,
    }
    if (origin_url and origin_url != url) or (not origin_url and link.get("url") != url):
        broken["checked_url"] = url  # Only include if different from original
    broken_links.append(broken)

def test_value(link, depth=0, origin_url=None, origin_file=None):
    """
    Checks if the url key is an object or not. If it is, iterate through every link in the object
    and check the URL for expected responses by calling check_url(link, url). If check fails, the
    entire object (with just the broken link) will be written to broken_links.json by the
    record_broken_link(link, url, error, origin_url, origin_file) function.

    Args: 
        link (dictionary): dictionary object containing key value pairs ('url': 'www.theurl.com')
                            that need to be tested.
        depth (int): number of redirections a link has caused
        origin_url (str, optional): The original URL from the source data.
        origin_file (str, optional): The original file from the source data.

    Returns: 
        None, outputs to console, writes to redirected_links.txt or broken_links.json
    """
    if depth > 3:
        print(f"Max recursion depth reached for link: {origin_url or link.get('url')}")
        broken = {
            "file": origin_file or link.get("file"),
            "url": origin_url or link.get("url"),
            "Error": "Max recursion depth reached for link."
        }
        broken_links.append(broken)
        return
    
    # Set origin_url and origin_file if not already set
    if origin_url is None:
        origin_url = link.get("url")
    if origin_file is None:
        origin_file = link.get("file")

    try:
        url_value = link['url']
        if isinstance(url_value, dict):
            for lang, url in url_value.items():
                check_url(link, url, depth, origin_url, origin_file)
        else:
            check_url(link, url_value, depth, origin_url, origin_file)
    except requests.RequestException as e:
        print(f"{type(e)} -> Error while checking URL {link['url']}: {e}\n")
        record_broken_link(link, url, str(e), origin_url, origin_file)

def check_url(link, url, depth=0, origin_url=None, origin_file=None):
    """
    Tests an individual link for a valid HTTP response (not 404 or other Error). 
    Redirection chains are logged in redirected_links.txt.
    Broken links are logged in broken_links.json.

    Args: 
        link (dictionary): dictionary object containing key value pairs ('url': 'www.theurl.com')
            that need to be tested.
        url (dictionary, string): The url string to be tested for a valid response.
        depth (int): number of redirections a link has caused
        origin_url (str, optional): The original URL from the source data.
        origin_file (str, optional): The original file from the source data.

    Returns: 
        None, outputs to console, writes to redirected_links.txt or broken_links.json
    """
    try:
        # Parse the URL to get the domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Check if the domain is from the ASCD site
        if((domain != '') and (domain != None) and (domain[0] != '#')):
            with requests.Session() as session:
                session.max_redirects = 10  # Safeguard against infinite redirects
                response = session.get(url, allow_redirects=False, timeout=10)

                # Check if initial response is a 404
                if response.status_code != 200:
                    print(f"Initial Code is NOT 200 at {url}")

                    # Manually handle redirects if 404 is detected initially
                    while response.status_code in [301, 302, 303, 307, 308]:
                        redirect_url = response.headers["Location"]
                        print(f"Redirecting to {redirect_url}")
                        response = session.get(
                            redirect_url, allow_redirects=False, timeout=10
                        )

                    # Final URL status check
                    if response.status_code == 200:
                        print(f"Successfully redirected to {response.url} with status 200\n")
                        redirected_links.append(url + " Redirected to: " + response.url) #redirection chain ended
                    elif response.status_code == 404:
                        # If 404, add to the broken_links list
                        record_broken_link(link, url, '404 Status Code', origin_url, origin_file)
                    else:
                        print(f"Ended with status {response.status_code} at {response.url}\n")
                else:
                    print(f"Ended with status code {response.status_code} at {url}\n")

    except requests.ConnectionError as e:
        print(f"Connection error while checking URL {url}. Treating as 404. ERROR: {e}\n")
        record_broken_link(link, url, str(e), origin_url, origin_file)
    except requests.Timeout as e:
        print(f"Timeout for URL {url}. Treating as 404. ERROR: {e}\n")
        record_broken_link(link, url, str(e), origin_url, origin_file)
    except requests.exceptions.MissingSchema as e:
        print(f"Missing Schema: {url}. ERROR: {e}\n")
        
        # Use regex to capture the missing part from the error message
        match = re.search(r"Invalid URL '([^']+)'", str(e))
        if match:
            missing_path = match.group(1)
            new_URL = "https://" + domain + missing_path
            print(f"The new URL is: {new_URL}\n")
            test_value({"url": new_URL}, depth = depth + 1, origin_url=origin_url, origin_file=origin_file)  # Pass as a dictionary with the new URL for testing
        else:
            print("Could not extract missing path from the error message.") 
    
try:
    file_path = get_file_path()
    valid_json_path = validate_json_file(file_path)
    print(f"File validated: {valid_json_path}")

    json_data = open(valid_json_path, encoding='utf-8-sig').read()

    # Convert the JSON string into a Python dictionary
    data = json.loads(json_data)

    # List to keep track of entries with 404 status
    broken_links = []

    #List to keep track of final URL after redirection chain
    redirected_links = []

    #prompt the user for the object to parse
    array_name = input("Please type the name of the array you wish to parse: ")

    # Loop through each link in the JSON
    for link in data[array_name]:
        test_value(link)

    # Print or save the broken links as needed
    with open('broken_links.json', 'w') as f:
        if(len(broken_links) > 0):
            f.write(json.dumps(broken_links, indent=4))
    
    #Save redirection chains to check where each link ends
    with open('redirected_links.txt', 'w') as f:
        if(len(redirected_links) > 0):
            for link in redirected_links:
                f.write(link + "\n")

except ValueError as e:
    print(e)
