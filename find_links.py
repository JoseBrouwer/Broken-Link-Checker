import os
from bs4 import BeautifulSoup
import json

# Directory containing the HTML files (you can place this file right in the project and remove it once you are done)
directory = "./content"

common = ""

# Output file
output_file = "extracted_links.txt"

def folders():
    with open(output_file, "w", encoding="utf-8") as outfile:
        
        for folder in os.listdir(directory):
            #print("in folder: " + folder)
            folderPath = directory + "/" + folder
            
            if os.path.isdir(folderPath):
                
                for filename in os.listdir(folderPath):
                    
                    if filename.endswith(".html"):
                        #print("reading file: " + filename)
                        filepath = os.path.join(folderPath, filename)

                        with open(filepath, 'r', encoding='utf-8') as html_file:
                            soup = BeautifulSoup(html_file, 'html.parser')
                            for a_tag in soup.find_all('a', href=True):
                                link = str(a_tag['href'])
                                title = ' '.join(a_tag.get_text().split())
                                if link[0] == "#" or link == "../../":
                                    continue
                                writeOut = (f"\n{link}\n {filename}")
                                outfile.write(f"{writeOut}\n--")

def no_folders():
    with open(output_file, "w") as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                unit_number = "unit" + filename.split('.')[0][0]
                filepath = os.path.join(directory, filename)
                
                with open(filepath, 'r', encoding='utf-8') as html_file:
                    soup = BeautifulSoup(html_file, 'html.parser')
                    for a_tag in soup.find_all('a', href=True):
                        link = str(a_tag['href'])
                        title = ' '.join(a_tag.get_text().split())
                        if link[0] == "#" or link == "../../":
                            continue
                        writeOut = (f"\n{link}\n {title}\n {unit_number}")
                        outfile.write(f"{writeOut}\n--")

def uses_api():
    with open(output_file, "w") as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                #unit_number = "unit" + filename.split('.')[0][0]
                filepath = os.path.join(directory, filename)
                
                ids = get_linkIds(filepath)
                    
def get_linkIds(filepath):
    values = []
    #Get a list of ids to search in links.json
    with open(filepath, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        #Find all a tags with a link and span tags with the data-linkApi-id class.
        #for tags in soup.find_all(['a', 'span'], href=True, attrs={"class": "data-linkApi-id"}):
        
        #soup.find_all returns a list of HTML elements matching <span data-linkApi-id...>
        #span_tag is an entry in this list which I treat as a string
        for span_tag in soup.find_all('span', 'data-linkApi-id'):
            tag_string = str(span_tag)
            value_string = ""

            value_location = tag_string.find('"') + 1 #first index of digit
            for char in tag_string[value_location:]:
                if char.isdigit():
                    value_string.append(char)
                else:
                    continue
            
            value = int(value_string) #cast to int
            values.append(value) #add to list
    return values

def search_json(ids):
    json_path = input("Provide the absolute path of the JSON file:")
    #with open(json_path, 'r', encoding='utf-8') as json_file
    


def parse_extracted():
    with open("extracted_links.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Process each link and store in a list in Mark's format
    links = []
    linkId = 0
    current_link = []

    for line in lines:
        if line.strip() == "--":  # End of a link entry
            if current_link:
                url = current_link[0]
                page = current_link[1]
                link = {
                    "linkId": f"{linkId}", 
                    "url": url, 
                    "page": page
                }
                links.append(link)
                linkId += 1
                current_link = []  # Reset for the next link
        else:
            if line.strip():  # Add non-empty lines to current link
                current_link.append(line.strip())

    # Create a dictionary to store the links
    data = {"links": links}

    # Write the data to a JSON file in the 'data' directory
    with open(os.path.join("data", "links2.json"), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def main(flag):
    match flag:
        case "-f":
            folders()
        case "-nf":
            no_folders()
        case "-api":
            uses_api()
    parse_extracted()