from datetime import datetime
import os
from typing import Set, Dict, List, Optional
import re


debug = 'DEBUG'
info = 'INFO'
warning = 'WARNING'
error = 'ERROR'
critical = 'CRITICAL'

class Error:
    def __init__(self, trace_id: str, name: str, text: str, date: str, user_name: Optional[str], level = info):
       
        self.trace_id: str = str(trace_id)
        self.name: str = name [:128]
        self.text: str = text [:1024]
        self.date = datetime.strptime(date, "%Y/%m/%d %H:%M") 
        self.user_name: Optional[str] = user_name if user_name is not None else None
        self.level: str = level

class Text_Logger_Provider:
    def __init__(self, log_folder: str = 'AppLog' ):
        self.log_folder: str = log_folder
        self.file_path: str = os.path.join(self.log_folder, f"{datetime.now().strftime('%Y_%m_%d')}.txt")

        self.logged_ids: Set[str] = self.existing_ids()
        self.logs_levels: Dict[str, List[str]] = None
        
#Making a folder AppLog
        os.makedirs(self.log_folder, exist_ok=True) 


#Load existing trace ids from the file into a set           
    def existing_ids(self) -> Set[str]:
        trace_ids: Set[str] = set()
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                for line in f:
                    if "Trace ID:" in line:
                        trace_id: str = line.split("Trace ID:")[1].split()[0]
                        trace_ids.add(trace_id)
        return trace_ids
    

    def raise_error(self, error_obj: Error) -> None:
        an_error: str = (
            f"Trace ID: {error_obj.trace_id} "
            f"Name: {error_obj.name} "
            f"Text: {error_obj.text} "
            f"Date: {error_obj.date.strftime('%Y/%m/%d %H:%M')} " 
            f"User Name: {error_obj.user_name if error_obj.user_name else 'None'} " 
            f"Level: {error_obj.level}\n"
        )

        if error_obj.trace_id in self.logged_ids:
            raise ValueError(f"Trace ID {error_obj.trace_id} already exists in the file.")
        else:
            with open(self.file_path, 'a') as f:
                f.write(an_error)

            self.logged_ids.add(error_obj.trace_id)

        if error_obj.level not in self.logs_levels:
            self.logs_levels[error_obj.level] = []
        self.logs_levels[error_obj.level].append(an_error.strip())


    def load_logs_by_level(self) -> Dict[str, List[str]]:
        if self.logs_levels:
            return self.logs_levels
        
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                for line in f:
                    level: Optional[str] = self.extract_log_level(line)
                    if level:
                        if level not in self.logs_levels:
                            self.logs_levels[level] = []
                        self.logs_levels[level].append(line.strip())
        return self.logs_levels

    def extract_log_level(self, line: str) -> Optional[str]:
        match = re.search(r"Level:\s*(\w+)", line)
        if match:
            return match.group(1)
        return None
    
    def print_to_console(self, level: str) -> None:
        logs_levels: Dict[str, List[str]] = self.load_logs_by_level()
        if level in logs_levels:
            for log in logs_levels[level]:
                print(log)
        else:
            print(f"No logs found for level: {level}")

    def get_logs_to_file(self, level: str, logs_file: str) -> None:
        logs_levels: Dict[str, List[str]] = self.load_logs_by_level()
        if level in logs_levels:
            with open(logs_file, 'a') as f:
                for log in logs_levels[level]:
                    f.write(log + '\n')
        else:
            print(f"No logs found for level: {level}")


    def clear_logs(self) -> None:
        if os.path.exists(self.log_folder):
            for file_name in os.listdir(self.log_folder):
                file_path: str = os.path.join(self.log_folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        self.logged_ids.clear()
        self.logs_levels.clear()
        
        self.file_path = os.path.join(self.log_folder, f"{datetime.now().strftime('%Y_%m_%d')}.txt")



if __name__ == "__main__":
    error_example = Error(
        trace_id = "001", 
        name = "NullPointerError", 
        text = "Attempt to dereference null pointer.", 
        date = "2024/02/12 10:15", 
        user_name = "Alice", 
        level = debug
        )

    logger_provider = Text_Logger_Provider()

    logger_provider.raise_error(error_example)
