# How To Use: 
- Simply double click `broken-link-checker.py`
    -  This will open the windows file explorer
- Select the JSON file that contains the links you want to parse
    - Note the file MUST be in JSON format
    - All the JSON file needs to include is a key labeled `url` to check the website
- The program will run it's course printing to the terminal when a site is considered broken
    - For resons other than an immediate 404 status code, additional context will be provided.
- Output is placed in broken_links.json in the same format provided

# Requires an installation of Python to use