import csv
import re

input_path = "../test/stubIdsBits.out"
output_path = "ttbarTracksOutputsBits.csv"

event_re = re.compile(r"event number:\s*(\S+)", re.IGNORECASE)
sector_re = re.compile(r"sector:\s*(\S+)", re.IGNORECASE)

current_event = None
current_sector = None

with open(input_path, "r") as infile, open(output_path, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    # optional header — adjust based on how many value columns you expect
    # writer.writerow(["event", "sector", "value..."])

    for line in infile:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        event_match = event_re.match(line)
        if event_match:
            current_event = event_match.group(1)
            continue

        sector_match = sector_re.match(line)
        if sector_match:
            current_sector = sector_match.group(1)
            continue

        # this is a "value" line — split on whitespace into columns
        values = line.split()
        writer.writerow([current_event, current_sector] + values)

print(f"Done. Wrote to {output_path}")