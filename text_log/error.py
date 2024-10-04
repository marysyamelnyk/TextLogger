from typing import Optional
from datetime import datetime

class Error:
    def __init__(self, trace_id: str, name: str, text: str, date: str, user_name: Optional[str], level = "INFO"):
       
        self.trace_id: str = str(trace_id)
        self.name: str = name [:128]
        self.text: str = text [:1024]
        self.date = datetime.strptime(date, "%Y/%m/%d %H:%M") 
        self.user_name: Optional[str] = user_name if user_name is not None else None
        self.level: str = level