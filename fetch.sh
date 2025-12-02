
set -euo pipefail
echo "Executing for "$(date "+%b %-d")

# Get today's day-of-month as number (no leading zero)
today=$(date +%-d)

# Input URL
url_in="https://adventofcode.com/2025/day/$today/input"

# Output file
path="inputs/dec${today}.txt"

# Save to file
if [ ! -f "$path" ]; then
    echo "Fetching data from AoC"
    curl --cookie "session=$AOC_SESSION" "$url_in" > "$path"
fi

# Source file things
src_file="src/dec${today}.py"
if [ ! -f "$src_file" ]; then
    echo "Creating source file"
    echo 'from utils.file import *
    
PATH = "'$path'"' >> "$src_file"

fi 
