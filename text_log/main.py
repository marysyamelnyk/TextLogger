from typing import Optional
from datetime import datetime
from text_log.logger import Text_Logger_Provider
from text_log.db import init_db, get_db

class Error:
    def __init__(self, trace_id: str, name: str, text: str, date: str, user_name: Optional[str], level = "INFO"):
       
        self.trace_id: str = str(trace_id)
        self.name: str = name [:128]
        self.text: str = text [:1024]
        self.date = datetime.strptime(date, "%Y/%m/%d %H:%M") 
        self.user_name: Optional[str] = user_name if user_name is not None else None
        self.level: str = level


if __name__ == "__main__":
    init_db()

    error_example = Error(
        trace_id = "001", 
        name = "NullPointerError", 
        text = "Attempt to dereference null pointer.", 
        date = "2024/02/12 10:15", 
        user_name = "Alice", 
        level = "DEBUG"
    )

    db = next(get_db())
    logger_provider = Text_Logger_Provider(db=db)

    logger_provider.raise_error(error_example)

    logger_provider.print_to_console("ERROR")
