import re
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

with open(input_file_path, "r") as f:
    lines = f.readlines()

output = ""
host = ""
ports = ""

for line in lines:
    if "shodan-api: Report for" in line:
        # Use a regular expression to extract the host IP address
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        if match:
            host = match.group(1)
        if host != "":
            output += f"Host: {host}   Ports: {ports.rstrip(', ')}\n"
            ports = ""
    elif "Host script results:" in line:
        continue
    elif "|" in line:
        line = line.strip().replace("|", "")
        # Check if the line contains "PORT PROTO PRODUCT VERSION"
        if "PORT PROTO PRODUCT VERSION" in line:
            continue  # Skip this line
        port = line.split()[0].lstrip("_")  # Remove "_" from the beginning of the port number
        protocol = line.split()[1] if len(line.split()) > 1 else ""
        version = line.split()[2] if len(line.split()) > 2 else ""
        ports += f"{port}//{protocol}//{version}/   , "

if host != "":
    output += f"Host: {host}   Ports: {ports.rstrip(', ')}\n"

# Remove the string "PORT//PROTO//PRODUCT/   ," from output.txt
with open(output_file_path, "w") as f:
    f.write(output)

# Remove duplicate lines from output.txt
lines_seen = set()
output_lines = []
with open(output_file_path, "r") as f:
    for line in f:
        if line not in lines_seen:
            lines_seen.add(line)
            output_lines.append(line)

with open(output_file_path, "w") as f:
    f.writelines(output_lines)

print(f"Processed and saved to {output_file_path}")
