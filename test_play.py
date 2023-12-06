import unittest
from unittest.mock import patch
from io import StringIO
from play import print_help_exit

class TestPlay(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_help_exit(self, mock_stdout):
        expected_output = """Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]

Option                  Behaviour (* = mutually-exclusive)
------                  ----------------------------------
none                    Use a random solution from the official Wordle dictionary
--today                 * Use today's official Wordle solution
DAY (number)            * Use the official solution from this DAY
SOLUTION (string)       * Use a given SOLUTION (must be 5-letter word)
--hints                 After each guess, report number of possible words remaining
-h, --help              Print this help text and quit
"""
        print_help_exit()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()