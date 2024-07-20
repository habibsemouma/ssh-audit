import re
import json
from datetime import datetime

class Session():
    def __init__(self,start_datetime=None,end_datetime=None,local_user=None,remote_user=None,process_id=None,ip_address=None,local_port=None) -> None:
        self.start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S.%f%z")  if start_datetime else None
        self.end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S.%f%z") if end_datetime else None
        self.local_user = local_user
        self.remote_user = remote_user
        self.process_id = process_id
        self.ip_address=ip_address
        self.local_port = local_port
    def to_json(self)->dict:
        return {
            "start_datetime": self.start_datetime if self.start_datetime else None,
            "end_datetime": self.end_datetime if self.end_datetime else None,
            "local_user": self.local_user,
            "remote_user": self.remote_user,
            "process_id": self.process_id,
            "ip_address": self.ip_address,
            "local_port": self.local_port
        }


def process_sessions(keys_filepath,log_filepath):
    sessions=[]
    
    users={key_idx:user_id for (key_idx, user_id) in enumerate([username.split("==")[1].replace("\n","") for username in open(keys_filepath,"r").readlines()],start=1)}
    log_stream=open(log_filepath,"r").read()
    pids=set(re.findall( r'sshd\[(\d+)\]',log_stream))

    for process_id in pids:
        session=Session(process_id=process_id)
        start_session_pattern =  rf'\d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}\.\d{{6}}\+\d{{2}}:\d{{2}} srv\d+ sshd\[{process_id}\]: Accepted key RSA SHA256:.* found at /home/.*/\.ssh/authorized_keys:\d+' 
        end_session_pattern = rf'\d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}\.\d{{6}}\+\d{{2}}:\d{{2}} srv\d+ sshd\[{process_id}\]: pam_unix\(sshd:session\): session closed for user (.*)'
        ip_pattern = rf'\d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}\.\d{{6}}\+\d{{2}}:\d{{2}} srv\d+ sshd\[{process_id}\]: Connection from ([\d.]+) port (\d+) on ([\d.]+)'
        start_session_match = re.search(start_session_pattern, log_stream)
        end_session_match=re.search(end_session_pattern,log_stream)
        ip_match=re.search(ip_pattern,log_stream)
        print(start_session_match)

        if start_session_match:
            date = start_session_match.group(0)[:32]
            key_idx = int(start_session_match.group(0).split(':')[-1])
            session.local_user=users[key_idx]
            session.start_datetime=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
            
        if end_session_match:
            end_session_date=end_session_match.group(0)[:32]
            remote_user= end_session_match.group(1)
            session.end_datetime=datetime.strptime(end_session_date, "%Y-%m-%dT%H:%M:%S.%f%z")
            session.remote_user=remote_user
        
        if ip_match:
            ip_address=ip_match.group(1)
            local_port=ip_match.group(2)
            session.ip_address=ip_address
            session.local_port=local_port
        if session.start_datetime is not None and session.remote_user is not None:sessions.append(session.to_json())
    
    
    return sessions
            


