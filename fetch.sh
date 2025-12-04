
set -euo pipefail

# Pick day: argument if given, otherwise today
if [[ $# -gt 0 ]]; then
    today="$1"
else
    # Get today's day-of-month as number (no leading zero)
    today=$(date +%-d)
fi

echo "Executing for "$(date "+%b")" $today"

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

# Open firefox to the problem url
prob_url="https://adventofcode.com/2025/day/$today"
firefox "$prob_url"
