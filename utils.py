import re
import json
from datetime import datetime

log_stream=open('auth.log',"r").read()

pids=re.findall( r'sshd\[\d+\]',log_stream)



for process_id in pids:
    pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2} srv\d+ sshd\[\d+\]: Accepted key RSA SHA256:.* found at /home/.*/\.ssh/authorized_keys:\d+'
    match = re.search(pattern, log_stream)

    if match:
        # Extract datetime and integer
        datetime_str = match.group(1)
        integer_at_end = match.group(2)
        
        # Print extracted values
        print("Datetime:", datetime_str)
        print("Integer at end:", integer_at_end)
    else:
        print("No match found")