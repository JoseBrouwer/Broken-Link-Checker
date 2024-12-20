import requests
import json
import re
import os
from tkinter import Tk, filedialog
from urllib.parse import urlparse


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
    
def test_link(link):
    """
    Tests an individual link for a valid HTTP response (not 404 or other Error). 
    Redirection chains are logged in redirected_links.txt.
    Broken links are logged in broken_links.json.

    Args: 
        link (dictionary): dictionary object containing key value pairs ('url': 'www.theurl.com')
                            that need to be tested.

    Returns: 
        None, outputs to console, writes to redirected_links.txt or broken_links.json
    """
    try:
        # Parse the URL to get the domain
        parsed_url = urlparse(link['url'])
        domain = parsed_url.netloc

        # Check if the domain is from the ASCD site
        if((domain != '') and (domain != None) and (domain[0] != '#')):
            with requests.Session() as session:
                session.max_redirects = 10  # Safeguard against infinite redirects
                response = session.get(link['url'], allow_redirects=False, timeout=10)

                # Check if initial response is a 404
                if response.status_code != 200:
                    print(f"Initial Code is NOT 200 at {link['url']}")

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
                        redirected_links.append(link['url'] + " Redirected to: " + response.url) #redirection chain ended
                    elif response.status_code == 404:
                        # If 404, add to the broken_links list
                        print(f"Broken link: {link['url']}\n")
                        link['Error'] = '404 Status Code'
                        broken_links.append(link)
                    else:
                        print(f"Ended with status {response.status_code} at {response.url}\n")
                else:
                    print(f"Ended with status code {response.status_code} at {link['url']}\n")

    except requests.ConnectionError as e:
        print(f"Connection error while checking URL {link['url']}. Treating as 404. ERROR: {e}\n")
        link['Error'] = str(e)
        broken_links.append(link)
    except requests.Timeout as e:
        print(f"Timeout for URL {link['url']}. Treating as 404. ERROR: {e}\n")
        link['Error'] = str(e)
        broken_links.append(link)
    except requests.exceptions.MissingSchema as e:
        print(f"Missing Schema: {link['url']}. ERROR: {e}\n")
        
        # Use regex to capture the missing part from the error message
        match = re.search(r"Invalid URL '([^']+)'", str(e))
        if match:
            missing_path = match.group(1)
            new_URL = "https://" + domain + missing_path
            print(f"The new URL is: {new_URL}\n")
            test_link({"url": new_URL})  # Pass as a dictionary with the new URL for testing
        else:
            print("Could not extract missing path from the error message.")
    except requests.RequestException as e:
            print(f"{type(e)} -> Error while checking URL {link['url']}: {e}\n")
            link['Error'] = str(e)
            broken_links.append(link)    
    
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
        test_link(link)

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
