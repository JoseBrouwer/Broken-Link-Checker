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
    """
    if not file_path:  # Checks if the file path is not empty
        raise ValueError("No file selected.")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".json":
        return file_path
    else:
        raise ValueError("Unsupported file type. Please select a JSON file.")

def folders():
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

def uses_api():
    all_ids = {}
    with open(output_file, "w") as outfile:
        for filename in os.listdir(content_directory):
            if filename.endswith(".html"):
                filepath = os.path.join(content_directory, filename)
                file_ids = get_linkIds(filepath)
                all_ids[str(filename)] = file_ids # set key's (the file's) value to a list of ids
        
        print("Done getting IDs")
        links = search_json()
        
        # Iterate over each filename and its associated IDs
        for filename, file_ids in all_ids.items():
            for file_id in file_ids:
                str_file_id = str(file_id)
                # Search for the file_id in the links from the JSON file
                for link in links["links"]:
                    if link["linkId"] == str_file_id:
                        url = link["url"]
                        tags = link["tags"]
                        # Write the filename along with the other link data to the output file
                        outfile.write(f"{filename}\n")
                        outfile.write(f"{url}\n")
                        #outfile.write(f"Tags: {tags}\n")
                        outfile.write("--\n")
    print("Done Writing for API")
          
def get_linkIds(filepath):
    values = []
    #Get a list of ids to search in links.json
    with open(filepath, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        
        #soup.find_all returns a list of HTML elements matching <span data-linkApi-id...>
        #span_tag is an entry in this list which I treat as a string
        for span_tag in soup.find_all('span'):
            tag_string = str(span_tag)
            value_string = ""

            value_location = tag_string.find('"') + 1 #first index of digit
            for char in tag_string[value_location:]:
                if char == '"' or not char.isdigit():
                    break
                elif char.isdigit():
                    value_string = value_string + char
            
            if(value_string.isdigit()):
                value = int(value_string) #cast to int
                values.append(value) #add to list
    return values

def search_json():
    print("Provide the absolute path of the JSON file:")
    file_path = get_file_path(True)
    json_path = validate_json_file(file_path)
    
    with open(json_path, 'r', encoding='utf-8') as json_file:
        links = json.load(json_file)
        print("Done retrieving JSON contents")
        return links    

def parse_extracted():
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
    data_path = course_directory + "/data"
    # Write the data to a JSON file in the 'data' directory
    with open(os.path.join(data_path, "links2.json"), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please provide flags: '-f' , '-nf', or '-api'")
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
            case "-api":
                uses_api()
                parse_extracted()
            case default:
                print("Please provide flags: '-f' , '-nf', or '-api'")

