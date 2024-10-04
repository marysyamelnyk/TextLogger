from db import init_db, get_db
from error import Error



if __name__ == "__main__":
    init_db()

    from logger import Text_Logger_Provider

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
