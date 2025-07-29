import json
import re

with open('<File Path for log file>', 'r') as f:
    # Initialize a list to hold the log entries
    # and lists to hold the parsed components   
    # Lists to hold log entries
    log_entries = []
    # Initialize lists to hold parsed components
    # Each list corresponds to a component of the log entry
    # Lists to hold parsed log components 
    timestamps = []
    hostnames = []
    process_names = []
    messages = []
    source_ip = []
    username = []
    outcome = []
    port = []

    # Read the file line by line
    # and parse each line into its components
    # Use regex to extract specific patterns
    for line in f:
        timestamps.append(" ".join(line.split()[:3]))
        hostnames.append(" ".join(line.split()[3:4]))
        process_names.append(" ".join(line.split()[4:5]))
        messages.append(" ".join(line.split()[5:]))
        # Use regex to extract specific patterns
        outcomes = re.search(r"(Failed|Accepted)", line)
        if outcomes:
            outcome.append(outcomes.group(1))
        else:
            outcome.append("Unknown")
        source_ips = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if source_ips:
            source_ip.append(source_ips.group(1))
        else:
            source_ip.append("Unknown")
        usernames = re.search(r'for (?:invalid user )?(\w+)', line)
        if usernames:
            username.append(usernames.group(1))
        else:
            username.append("Unknown")
        port_match = re.search(r'port (\d+)', line)
        if port_match:
            port.append(port_match.group(1))
        else:
            port.append("Unknown")
        entry = {
            "timestamp": timestamps[-1],
            "hostname": hostnames[-1],
            "process_name": process_names[-1],
            "message": messages[-1],
            "source_ip": source_ip[-1],
            "username": username[-1],
            "outcome": outcome[-1],
            "port": port[-1]
        }
        log_entries.append(entry)
        
# Save the parsed log entries to a JSON file
with open('normalized_logs.json', 'w') as outfile:
    json.dump(log_entries, outfile, indent=2)
