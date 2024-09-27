from datetime import datetime
import os
from typing import Set, Dict, List, Optional
import re
from sqlalchemy.orm import Session
from text_log.models import ErrorModel
from text_log.main import Error


class Text_Logger_Provider:
    def __init__(self, log_folder: str = 'AppLog', db: Optional[Session] = None ):
        self.log_folder: str = log_folder
        self.file_path: str = os.path.join(self.log_folder, f"{datetime.now().strftime('%Y_%m_%d')}.txt")
        self.db = db

        self.logged_ids: Set[str] = self.existing_ids()
        self.logs_levels: Dict[str, List[str]] = None
        
        os.makedirs(self.log_folder, exist_ok=True) 

          
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


        if self.db:
            db_error = ErrorModel(
                trace_id = error_obj.trace_id,
                name = error_obj.name,
                text = error_obj.text,
                date = error_obj.date,
                user_name = error_obj.user_name,
                level = error_obj.level
            )

            existing_error = self.db.query(ErrorModel).filter_by(trace_id = error_obj.trace_id).first()
            if existing_error:
                raise ValueError(f"Trace ID {error_obj.trace_id} already exists in the database.")
            
            self.db.add(db_error)
            self.db.commit()

        if error_obj.level not in self.logs_levels:
            self.logs_levels[error_obj.level] = []
        self.logs_levels[error_obj.level].append(an_error.strip())


    def load_logs_by_level(self, level: str) -> Dict[str, List[str]]:
        if self.logs_levels:
            return self.logs_levels
    
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                for line in f:
                    level_in_line: Optional[str] = self.extract_log_level(line)
                    if level_in_line:
                        if level_in_line not in self.logs_levels:
                            self.logs_levels[level_in_line] = []
                        self.logs_levels[level_in_line].append(line.strip())
    
        if self.db:
            db_logs = self.db.query(ErrorModel).filter(ErrorModel.level == level).all()

            for log in db_logs:
                log_entry = (
                    f"Trace ID: {log.trace_id} "
                    f"Name: {log.name} "
                    f"Text: {log.text} "
                    f"Date: {log.date.strftime('%Y/%m/%d %H:%M')} "
                    f"User Name: {log.user_name} "
                    f"Level: {log.level}"
                )
                if log.level not in self.logs_levels:
                    self.logs_levels[log.level] = []
                self.logs_levels[log.level].append(log_entry)

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

        if self.db:
            self.db.query(ErrorModel).delete()
            self.db.commit()





