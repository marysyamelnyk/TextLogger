import os
import unittest
from unittest.mock import mock_open, patch
from typing import Set

class ErrorLogger:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def existing_ids(self) -> Set[str]:
        trace_ids: Set[str] = set()
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                for line in f:
                    if "Trace ID:" in line:
                        trace_id: str = line.split("Trace ID:")[1].split()[0]
                        trace_ids.add(trace_id)
        return trace_ids

class TestErrorLogger(unittest.TestCase):
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="Some log info\nTrace ID: 12345\nTrace ID: 67890\nOther info\nTrace ID: 54321\n")
    def test_existing_ids(self, mock_open, mock_exists):
        mock_exists.return_value = True
        logger = ErrorLogger("/fake/path/to/log.txt")
        result = logger.existing_ids()
        
        expected_ids = {"12345", "67890", "54321"}
        self.assertEqual(result, expected_ids)

        mock_open.assert_called_once_with("/fake/path/to/log.txt", 'r')

    @patch("os.path.exists", return_value = False)
    def test_existinf_ids_no_file(self, mock_exists):
        logger = ErrorLogger("/fake/path/to/non_existent_log.txt")
        result = logger.existing_ids()

        self.assertEqual(result, set())
        mock_exists.assert_called_once_with("/fake/path/to/non_existent_log.txt")




        


if __name__ == '__main__':
        unittest.main()    