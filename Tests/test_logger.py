import os
import unittest
from unittest.mock import mock_open, patch
from text_log.logger import Text_Logger_Provider

class Test_Text_Logger_Provider(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'test_file.log'
        self.instance = Text_Logger_Provider(self.file_path)


    @patch('builtins.open', new_callable=mock_open, read_data="Trace ID: 12345\nSome other line\nTrace ID: 67890\n")
    def test_existing_ids(self, mock_file):
        result = self.instance.existing_ids()

        expected_ids = {"12345", "67890"}
        self.assertEqual(result, expected_ids)
        mock_file.assert_called_once_with(self.file_path, 'r')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Trace ID: 12345\n")
    def test_existing_ids_with_one_id(self, mock_file, mock_exists):
        result = self.instance.existing_ids()

        expected_ids = {"12345"}
        self.assertEqual(result, expected_ids)

    @patch('os.path.exists', return_value=False)
    def test_existing_ids_no_file(self, mock_exists):
        result = self.instance.existing_ids()

        self.assertEqual(result, set())


    if __name__ == '__main__':
        unittest.main()