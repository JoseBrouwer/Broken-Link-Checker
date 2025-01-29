import os
import sys
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog
import json

#Course folder
course_directory = ""

# Place directory containing the HTML files here
content_directory = ""

# Output file
output_file = "extracted_links.txt"

def get_file_path(file):
    """
    Opens a file selection dialog and returns the selected file path.

    Args: 
        file (boolean): True if searching for a file, False for a folder

    Returns:
        string: the path to the file
    """
    root = Tk()
    root.withdraw()  # Hide the main window
    if(file):
        file_path = filedialog.askopenfilename()
    else:
        file_path = filedialog.askdirectory()
    root.destroy() # Close the main window
    return file_path


def validate_json_file(file_path):
    """
    Checks if the selected file is a JSON file. If it is, return the file path,
    otherwise, raise a ValueError.

    Args:
        file_path (string): the file to validate as a JSON

    Returns:
        string: file_path if valid
        valueError: file_path is not valid
    """
    if not file_path:  # Checks if the file path is not empty
        raise ValueError("No file selected.")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".json":
        return file_path
    else:
        raise ValueError("Unsupported file type. Please select a JSON file.")

def folders():
    """
    Navigates folder structure for HTML files.
    Parses HTML files for anchor tags containing links that must be checked for validity.
    Writes the found links along with the file they were found on, in extracted_links.txt.

    Args:
        None

    Returns:
        None, writes to extracted_links.txt
    """
    if(content_directory != ""):
        with open(output_file, "w", encoding="utf-8") as outfile:
            for folder in os.listdir(content_directory):
                #print("in folder: " + folder)
                folderPath = content_directory + "/" + folder         
                if os.path.isdir(folderPath):            
                    for filename in os.listdir(folderPath):                 
                        if filename.endswith(".html"):
                            #print("reading file: " + filename)
                            filepath = os.path.join(folderPath, filename)
                            with open(filepath, 'r', encoding='utf-8') as html_file:
                                soup = BeautifulSoup(html_file, 'html.parser')
                                for a_tag in soup.find_all('a', href=True):
                                    url = str(a_tag['href'])

                                    outfile.write(f"{filename}\n")
                                    outfile.write(f"{url}\n")
                                    #outfile.write(f"Tags: {tags}\n")
                                    outfile.write("--\n")

def no_folders():
    """
    Navigates folder containing only HTML files.
    Parses HTML files for anchor tags containing links that must be checked for validity.
    Writes the found links along with the file they were found on, in extracted_links.txt.

    Args:
        None

    Returns:
        None, writes to extracted_links.txt
    """
    if(content_directory != ""):
        with open(output_file, "w") as outfile:
            for filename in os.listdir(content_directory):
                if filename.endswith(".html"):
                    unit_number = "unit" + filename.split('.')[0][0]
                    filepath = os.path.join(content_directory, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as html_file:
                        soup = BeautifulSoup(html_file, 'html.parser')
                        for a_tag in soup.find_all('a', href=True):
                            url = str(a_tag['href'])

                            outfile.write(f"{filename}\n")
                            outfile.write(f"{url}\n")
                            #outfile.write(f"Tags: {tags}\n")
                            outfile.write("--\n")

def parse_extracted():
    """
    parses extracted_links.txt into a JSON format parallel to the one expected by
    broken-link-check.py.

    Args:
       None

    Returns:
        None, writes to links2.json and deletes extracted_links.txt
    """
    if(content_directory != ""):
        with open("extracted_links.txt", "r", encoding="utf-8", errors="replace") as file:
            lines = file.readlines()

        # Process each link and store in a list in Mark's format
        links = []
        current_link = []

        for line in lines:
            if line.strip() == "--":  # End of a link entry
                if current_link:
                    file = current_link[0]
                    url = current_link[1]
                    link = {
                        "file": file,
                        "url": url
                    }
                    links.append(link)
                    current_link = []  # Reset for the next link
            else:
                if line.strip():  # Add non-empty lines to current link
                    current_link.append(line.strip())

        # Create a dictionary to store the links
        data = {"links": links}
        # Write the data to a JSON file in the 'data' directory
        with open("links2.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        os.remove("extracted_links.txt")

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please provide flags: '-f' or '-nf'")
    else:
        print("Select the directory containing the course")
        course_directory = get_file_path(False)

        print("select the directory containing the content")
        content_directory = get_file_path(False)

        flag = sys.argv[1] # get flags
        match flag:
            case "-f":
                folders()
                parse_extracted()
            case "-nf":
                no_folders()
                parse_extracted()
            case default:
                print("Please provide flags: '-f' or '-nf'")