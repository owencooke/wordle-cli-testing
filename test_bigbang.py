import unittest
from io import StringIO
import sys
from unittest.mock import MagicMock, patch  # Import patch for mocking
from play import play, print_help_exit  # Import your print_help_exit function


def get_print_args(mock):
    arg_list = [arg.args[0] if len(arg.args) != 0 else "" for arg in mock.call_args_list]
    return arg_list


class TestPrintHelpExit(unittest.TestCase):
    @patch('builtins.exit')  # Mock sys.exit
    def test_print_help_exit_output(self, mock_exit):
        # Redirect stdout to capture the output
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the function
        print_help_exit()

        # Get the printed content
        printed_content = captured_output.getvalue()

        # Restore the original stdout
        sys.stdout = sys.__stdout__

        # Define the expected output
        expected_output = (
            "Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]\n\n"
            "Option\t\t\tBehaviour (* = mutually-exclusive)\n"
            "------\t\t\t----------------------------------\n"
            "none\t\t\tUse a random solution from the official Wordle dictionary\n"
            "--today\t\t\t* Use today's official Wordle solution\n"
            "DAY (number)\t\t* Use the official solution from this DAY\n"
            "SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)\n"
            "--hints\t\t\tAfter each guess, report number of possible words remaining\n"
            "-h, --help\t\tPrint this help text and quit\n"
        )

        # Assert that the printed content matches the expected output
        self.assertEqual(printed_content, expected_output)

        # Assert that sys.exit was called with no argument (exit code 0)
        mock_exit.assert_called_with()

    @patch('sys.argv', ['test.py', '-h'])
    @patch("builtins.print")
    def test_h_argument(self, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual(["Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]",
                          "",
                          "Option\t\t\tBehaviour (* = mutually-exclusive)",
                          "------\t\t\t----------------------------------",
                          "none\t\t\tUse a random solution from the official Wordle dictionary",
                          "--today\t\t\t* Use today's official Wordle solution",
                          "DAY (number)\t\t* Use the official solution from this DAY",
                          "SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)",
                          "--hints\t\t\tAfter each guess, report number of possible words remaining",
                          "-h, --help\t\tPrint this help text and quit"], arg_list)

    @patch('sys.argv', ['test.py', '--help'])
    @patch("builtins.print")
    def test_help_argument(self, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual(["Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]",
                          "",
                          "Option\t\t\tBehaviour (* = mutually-exclusive)",
                          "------\t\t\t----------------------------------",
                          "none\t\t\tUse a random solution from the official Wordle dictionary",
                          "--today\t\t\t* Use today's official Wordle solution",
                          "DAY (number)\t\t* Use the official solution from this DAY",
                          "SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)",
                          "--hints\t\t\tAfter each guess, report number of possible words remaining",
                          "-h, --help\t\tPrint this help text and quit"], arg_list)

    @patch('sys.argv', ['test.py', '-invalid'])
    @patch("builtins.print")
    def test_invalid_argument(self, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual(["Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]",
                          "",
                          "Option\t\t\tBehaviour (* = mutually-exclusive)",
                          "------\t\t\t----------------------------------",
                          "none\t\t\tUse a random solution from the official Wordle dictionary",
                          "--today\t\t\t* Use today's official Wordle solution",
                          "DAY (number)\t\t* Use the official solution from this DAY",
                          "SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)",
                          "--hints\t\t\tAfter each guess, report number of possible words remaining",
                          "-h, --help\t\tPrint this help text and quit"], arg_list[1:])
        self.assertEqual("\x1b[33mInvalid argument -invalid\x1b[0m\xA0", arg_list[0])

    @patch('sys.argv', ['test.py', 'ABCDE'])
    @patch("builtins.print")
    def test_invalid_solution(self, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual(["Usage: python3 play.py [-h|--help] [--today|DAY|SOLUTION] [--hints]",
                          "",
                          "Option\t\t\tBehaviour (* = mutually-exclusive)",
                          "------\t\t\t----------------------------------",
                          "none\t\t\tUse a random solution from the official Wordle dictionary",
                          "--today\t\t\t* Use today's official Wordle solution",
                          "DAY (number)\t\t* Use the official solution from this DAY",
                          "SOLUTION (string)\t* Use a given SOLUTION (must be 5-letter word)",
                          "--hints\t\t\tAfter each guess, report number of possible words remaining",
                          "-h, --help\t\tPrint this help text and quit"], arg_list[1:])
        self.assertEqual("\x1b[33mInvalid solution ABCDE, must be a valid guess\x1b[0m\xA0", arg_list[0])

    @patch('sys.argv', ['test.py', 'AUDIO'])
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['AUDIO'])
    def test_fixed_solution(self, mock_input, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual("\x1b[33mSolution will be AUDIO\x1b[0m\xA0", arg_list[0])

    @patch('sys.argv', ['test.py', '--hints', '--today'])
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['AUDIO', 'AUDIO', 'AUDIO', 'AUDIO', 'AUDIO', 'AUDIO'])
    def test_today_hints_solution(self, mock_input, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual(
            '\x1b[43;30mA\x1b[0m\x1b[43;30mU\x1b[0m\x1b[40;37mD\x1b[0m\x1b[40;37mI\x1b[0m\x1b[40;37mO\x1b[0m '
            '\x1b[90m257 possible\x1b[0m\xa0', arg_list[1])

    @patch('sys.argv', ['test.py', '11'])
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['AUDIO', 'AUDIO', 'AUDIO', 'AUDIO', 'AUDIO', 'AUDIO'])
    def test_today_int_solution(self, mock_input, mock_print):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual('\x1b[1;31m🤦 LOSE! The solution was DWARF\x1b[0m\xa0', arg_list[-1])

    @patch('sys.argv', ['test.py'])
    @patch('random.choice', return_value='AUDIO')
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF',
                                          'DWARF', '', 'AUDIO', KeyboardInterrupt])
    def test_random_solution(self, mock_input, mock_print, mock_random):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual('\x1b[1;32m🤯 GENIUS! Got it in 1/6 rounds\x1b[0m\xa0', arg_list[-4])

    @patch('sys.argv', ['test.py'])
    @patch('random.choice', return_value='AUDIO')
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF',
                                          'DWARF', '', 'AUDIO', KeyboardInterrupt])
    def test_play_again(self, mock_input, mock_print, mock_random):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual('\x1b[1;32m🤯 GENIUS! Got it in 1/6 rounds\x1b[0m\xa0', arg_list[-4])

    @patch('sys.argv', ['test.py'])
    @patch('random.choice', return_value='AUDIO')
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF', EOFError])
    def test_eof_error(self, mock_input, mock_print, mock_random):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual('\x1b[1;31m🤦 LOSE! The solution was AUDIO\x1b[0m\xa0', arg_list[-2])

    @patch('sys.argv', ['test.py'])
    @patch('random.choice', return_value='AUDIO')
    @patch("builtins.print")
    @patch('builtins.input', side_effect=['DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF', 'DWARF', KeyboardInterrupt])
    def test_ctrl_c(self, mock_input, mock_print, mock_random):
        with self.assertRaises(SystemExit):
            play()
        arg_list = get_print_args(mock_print)
        self.assertEqual('\x1b[1;31m🤦 LOSE! The solution was AUDIO\x1b[0m\xa0', arg_list[-2])


if __name__ == '__main__':
    unittest.main()
