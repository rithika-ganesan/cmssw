import csv
import re
import sys

input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
output_path = sys.argv[2] if len(sys.argv) > 2 else "widths.csv"

pattern = re.compile(r"^\s*WIDTHS:\s*((?:\d+\s*)+)$")

with open(input_path) as infile, open(output_path, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    for line in infile:
        match = pattern.match(line)
        if match:
            writer.writerow(match.group(1).split())