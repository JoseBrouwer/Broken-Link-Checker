# Step 1: Install the requirements
Write-Host "Installing requirements from requirements.txt..."
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

# Step 2: Define default flags for find_links.py
$flag = ""
$apiFlag = ""
$noFlag = ""

# Step 3: Process command-line arguments
Param (
    [switch]$f,    # -f option
    [switch]$nf,   # -nf option
    [switch]$api   # -api option
)

# Check if the flags were passed and set the corresponding variables
if ($f) { $flag = "-f" }
if ($nf) { $noFlag = "-nf" }
if ($api) { $apiFlag = "-api" }

# Step 4: Run find_links.py with the provided flags
Write-Host "Running find_links.py with options..."
python .\find_links.py $flag $noFlag $apiFlag

# Step 5: Run broken-link-check.py (no flags provided)
Write-Host "Running broken-link-check.py..."
python .\broken-link-check.py
