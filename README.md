# How To Use: 
1. Run `find_links.py` and select the following in this order, using the file explorer that comes up: 
    1. Directory containing the course
    2. Directory containing the course content
    - If using `-api` flag:
    3. links.json file in the data folder
2. This will output `links2.json` in the data folder for the course
3. Run `broken-link-checker.py`
    -  This will open the windows file explorer
4. Select the JSON file that contains the links you want to parse (`data/links2.json`)
    - Note the file MUST be in JSON format
    - All the JSON file needs to include is a key labeled `url` to check the website
    - The program will run it's course printing to the terminal when a site is considered broken
    - For resons other than an immediate 404 status code, additional context will be provided
    - Output is placed in broken_links.json in the same format provided
5. In the same directory as the `broken-link-check.py` you will find `broken_links.json` file, containing all of the links deemed 'broken' along with the error. 
6. The `file` key indicates the HTML file that conatins the link. You must match this file to the url assigned in the `data/Pages.json` file. 
    - This is because the HTML file does NOT match the url on the live course. 

# Requires an installation of Python to use