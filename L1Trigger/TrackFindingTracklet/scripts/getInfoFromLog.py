#!/usr/bin/env python3
"""Usage: python parse_stubs.py cmsRun.log stubs.csv"""
import csv
import re
import sys

RECORD_RE = re.compile(r"Begin processing the (\d+)(?:st|nd|rd|th) record")
SECTOR_RE = re.compile(r"Sector:\s*(\d+)")
KV_RE = re.compile(r"(\w+)=(\S+)")

# FLAG = "TRUTHSTUBINFO"
FLAG = "DRINFO"


def main(log_path, csv_path):
    record = 0     # stays 0 if a line appears before any "Begin processing"
    sector = ""    # stays empty until a "sector: <num>" line has been seen
    rows = []
    columns = ["record", "sector"]

    with open(log_path, errors="replace") as f:
        for line in f:
            m = RECORD_RE.search(line)
            if m:
                record = int(m.group(1))
                sector = ""   # a new record starts without a known sector
                continue

            # no 'continue' here, so a sector and a FLAG on the same line both work
            s = SECTOR_RE.search(line)
            if s:
                sector = int(s.group(1))

            idx = line.find(FLAG)
            if idx == -1:
                continue

            row = {"record": record, "sector": sector}
            for key, value in KV_RE.findall(line[idx + len(FLAG):]):
                row[key] = value
                if key not in columns:
                    columns.append(key)
            rows.append(row)

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, restval="")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {csv_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python parse_stubs.py <input_log> <output_csv>")
    main(sys.argv[1], sys.argv[2])