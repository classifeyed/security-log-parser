import json
import re

with open('<File Path for log file>', 'r') as f:

    # Lists to hold log entries
    log_entries = []

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
            username.append(usernames.group(0))
        else:
            username.append("Unknown")
        port_match = re.search(r'port (\d+)', line)
        if port_match:
            port.append(port_match.group(1))
        else:
            port.append("Unknown")


    # for i in range(len(timestamps)):
    #    print(f"{timestamps[i]} | {hostnames[i]} | {process_names[i]} | {messages[i]} | {source_ip[i]} | {username[i]} | {outcome[i]}")
    # Close the file after reading
    # f.close()

    for i in range(len(timestamps)):
        entry = {
            "timestamp": timestamps[i],
            "hostname": hostnames[i],
            "process_name": process_names[i],
            "message": messages[i],
            "source_ip": source_ip[i],
            "username": username[i],
            "outcome": outcome[i],
            "port": port[i]
        }
        log_entries.append(entry)

with open('normalized_logs.json', 'w') as outfile:
    json.dump(log_entries, outfile, indent=2)
