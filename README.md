# How To Use: 
1. Run `find_links.py` and select the following in this order, using the file explorer that comes up: 
    1. Directory containing the course
    2. Directory containing the course content
        - If using `-api` flag:
    3. links.json file in the data folder
2. This will output `links2.json` in the directory for this program
3. Run `broken-link-checker.py`
    -  This will open the windows file explorer
4. Select the JSON file that contains the links you want to parse (`links2.json`)
    - Note the file MUST be in JSON format
    - All the JSON file needs to include is a key labeled `url` to check the website
    - The program will run it's course printing to the terminal when a site is considered broken
    - For resons other than an immediate 404 status code, additional context will be provided
    - Output is placed in broken_links.json in the same format provided
5. In the same directory as the `broken-link-check.py` you will find `broken_links.json` file, containing all of the links deemed 'broken' along with the error. 
6. The `file` key indicates the HTML file that conatins the link. You must match this file to the url assigned in the `data/Pages.json` file. 
    - This is because the HTML file does NOT ALWAYS match the url on the live course.

## Note: 
- Sometimes websites are hijacked by malicious actors and redirect users to their websites. 
- For Example, say you go to **abc.com** but this website has been hijacked and redirects you to **gambling.com**. Now, it will rarely _(if ever)_ be this obviuous. Usually, URLs will look totally normal at a glance but when we go to the website it has undesireable content.
- ### How do I check for instances like this?
    - After you run `broken-link-check.py` a text file titled `redirected_links.txt` will appear in the folder for this program. This text file will contain the following text (one per line): 
    ```{URL} Redirected to {Redirected URL} ```
    - Clicking on the `Redirected URL` will take you to a links final destination. If this site looks off note the `URL` and find its location using `broken_links.json`. 

# Requires an installation of [Python](https://www.microsoft.com/store/productId/9NCVDN91XZQP?ocid=pdpshare) to use
- If you are on Windows the hyperlink on the word 'Python' will take you to the microsoft store. This is the easiest way to install Python on Windows.
