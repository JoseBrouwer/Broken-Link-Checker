import os
from bs4 import BeautifulSoup
import json


# Directory containing the HTML files (you can place this file right in the project and remove it once you are done)
directory = "./content"

# Output file
output_file = "extracted_links.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    for folder in os.listdir(directory):
        print("in folder: " + folder)
        folderPath = directory + "/" + folder
        
        if os.path.isdir(folderPath):
            
            for filename in os.listdir(folderPath):
                
                if filename.endswith(".html"):
                    
                    print("reading file: " + filename)
                    # unit_number = "unit" + filename.split('.')[0][0]
                    filepath = os.path.join(folderPath, filename)

                    with open(filepath, 'r', encoding='utf-8') as html_file:

                        soup = BeautifulSoup(html_file, 'html.parser')

                        for a_tag in soup.find_all('a', href=True):
                            link = str(a_tag['href'])
                            text = ' '.join(a_tag.get_text().split())
                            if link[0] == "#" or link == "../../":
                                continue
                            writeOut = (f"\n{link}\n {filename}")
                            outfile.write(f"{writeOut}\n--")


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