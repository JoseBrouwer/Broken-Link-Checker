# Requires an installation of [Python](https://www.microsoft.com/store/productId/9NCVDN91XZQP?ocid=pdpshare) to use
- If you are on Windows the hyperlink on the word 'Python' will take you to the microsoft store. This is the easiest way to install Python on Windows.
- Mac/Linux, you already have Python installed. 
- Check either installation by using these commands:
    ```
    Windows: python --version
    Mac/Linux: python3 --version
    ```
    You'll see something like this: `Python 3.10.12` depending on the version you have, this will vary. **Anything starting with 3 should be fine.**

# An installation of pip is required to use
- ## pip comes pre-installed on Windows through the Microsoft Store
- ## Mac is more involved: 
1. Install Homebrew (optional but recommended): If you don’t have Homebrew (a package manager for macOS), you can install it by running this in the Terminal:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install Python (if not already installed):
        - You can install Python 3, which comes with pip, using Homebrew:
        ```
        brew install python
        ```
3. Verify pip Installation: After installation, check if pip is installed:
    ```
    pip3 --version
    ```
4. Update pip: If needed, you can update pip to the latest version with:
    ```
    pip3 install --upgrade pip
    ```
5. **IMPORTANT**: You **MUST** change line 5 of `run.sh` to `pip3 install -r requirements.txt` to make the script work!!!
- ## Linux
1. Install Python (if not installed): Most Linux distributions come with Python pre-installed. To check, run:
    ```
    python3 --version
    ```
2. Install pip: You can install pip by running the following commands based on your Linux distribution.
    - Debian/Ubuntu: 
        ```
        sudo apt update
        sudo apt install python3-pip
        ```
    - Fedora:
        ```
        sudo dnf install python3-pip
        ```
    - Arch: 
        ```
        sudo pacman -S python-pip
        ```
3. Once installed, verify the installation with:
    ```
    pip3 --version
    ```
4. Update pip: You can update pip with:
    ```
    pip3 install --upgrade pip
    ```

# How To Use 
### (**NOTE**: these commands assume you are in the Broken-Link-Checker Directory when you call them): `<download-location>/Broken-Link_Checker`

## For Old Courses (No use of link API)
1. Depending on your Operating System you will use one of two files, run.ps1 or run.sh.
    - Look at the **course structure** to pick **FLAGS**: 
        - No folders: -nf
        - Folders: -f
    - Windows: `.\run.ps1 -nf` or `.\run.ps1 -f`
    - Mac/Linux: `chmod +x run.sh` then `./run.sh -nf` or `./run.sh -f`
    - ***NOTE Windows:*** Your Sys Admin may have blocked scripts from running on your computer for security purposes, if so follow `The Complete Process`. 
    - ***IMPORTANT:*** If you run the program using these scripts you do not need to use the commandline to run programs anymore. All of the program executions are done for you. The points below explain what to select and where to find the broken links.
2.  
- Windows:
    ```
    .\run.ps1 [Flag]
    ```
- Mac/Linux:
    ```
    ./run.sh [Flag]
    ```
3. select the folder(s) indicated on the terminal in sequential order, it may say the folder for the course, the content folder, the links.json file, or the links2.json
    - Depends on the selected flag, you should be prompted for a specific folder. If not, look at `The Complete Process` for detailed steps of what to do next
4. When you see `Running broken-link-check.py...` select the `links2.json` file in the `Broken-Link-Checker` folder on your computer
    - After all the correct files are selected, the links are tested
    - All broken links are found in `broken_links.json`
5. Check `redirected_links.txt` for any weird sites by clicking on the link to the right of `Redirected To`.
    - If this link takes you somewhere weird (gambling site, adult site, unrelated to course content) 
    - Then the link on the left of `Redirected to` must be incluided in the Broken Link Report

## Courses with the link API
1. Run `broken-link-check.py`:
- Windows: 
    ```
    python .\broken-link-check.py
    ```
- Mac/Linux:
    ```
    python3 ./broken-link-check.py
    ```
2. In the file explorer window that opens, select `data/<JSON File with links>` (usually `data/links.json`)
3. When prompted in the console, type the name of the array object you want to parse. This can be `links`, `resources`, `items`, etc. 
- See step 6 of `The Complete Process` for examples if you don't know what to look for.
4. Output is placed in `broken_links.json` in the same format provided

## The Complete Process
1. The first program we use is `find_link.py`.
    - We use it differently depending on the structure of the course: 
        - HTML files are ***not in*** folders within `<course-name>/content`:
            1. Windows: `python .\find_links.py -nf`
            2. Mac/Linux: `python3 ./find_links.py -nf`
        - HTML files are **in** folders within `<course-name>/content`:
            1. Windows: `python .\find_links.py -f`
            2. Mac/Linux: `python3 ./find_links.py -f`
        
2. Run `find_links.py` and select the following in this order, using the file explorer that comes up: 
    1. Directory containing the course
    2. Directory containing the course content
3. This will output `links2.json` in the directory for this program
4. Run `broken-link-check.py`
    -  This will open the windows file explorer
5. Select the JSON file that contains the links you want to parse (`links2.json` or `data/links.json`)
    - Note the file MUST be in JSON format
    - All the JSON file needs to include is a key labeled `url` to check the website
    - The program will run it's course printing to the terminal when a site is considered broken
    - For resons other than an immediate 404 status code, additional context will be provided
    - Output is placed in `broken_links.json` in the same format provided
6. The console will prompt you to type the name of the array object you want to parse.
    - Any use of the linkApi (usually newer BEESS courses) will usually be titled "links"
    - Other projects maybe titled "resources"
    - ***Check your JSON file for the correct object name***
    ```
    Example: links.json
        {
        vvvv THIS IS THE ARRAY OBJECT (has [])
        "links": [{
            "linkId": "1",
            "title": "Deciding to Teach Them All",
            "url": "http://www.ascd.org/publications/educational-leadership/oct03/vol61/num02/Deciding-to-Teach-Them-All.aspx",
            "tags": "etpswd,unit1,resource,tswd,tswd-unit3",
            "isExternal": true
            }]
        }
    ```
7. In the same directory as the `broken-link-check.py` you will find the `broken_links.json` file, containing all of the links deemed 'broken' along with the error. 
8. The `file` key indicates the HTML file that conatins the link. You must match this file to the url assigned in the `data/Pages.json` file ***(Suggested if content on webpage does not match html file).***

## Final step and its purpose 
- Sometimes websites are hijacked by malicious actors and redirect users to their websites. 
- For Example, say you go to **abc.com** but this website has been hijacked and redirects you to **gambling.com**. Now, it will rarely _(if ever)_ be this obviuous. Usually, URLs will look totally normal at a glance but when we go to the website it has undesireable content.
- ### How do I check for instances like these?
    - After you run `broken-link-check.py` a text file titled `redirected_links.txt` will appear in the folder for this program. This text file will contain the following text (one per line): 
    ```{URL} Redirected to {Redirected URL} ```
    - Clicking on the `Redirected URL` will take you to a links final destination. If this site looks off note the `URL` and find its location using `broken_links.json`. 
