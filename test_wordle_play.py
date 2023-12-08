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
    @patch('play.CLIPlayer')
    @patch("builtins.print")
    def test_invalid_argument(self, mock_print, mock_player):
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
                          "-h, --help\t\tPrint this help text and quit"], arg_list[0:])
        mock_player().warn.assert_called_once_with(f"Invalid argument -invalid")

    @patch('sys.argv', ['test.py', 'ABCDE'])
    @patch('play.CLIPlayer')
    @patch("builtins.print")
    def test_invalid_solution(self, mock_print, mock_player):
        with self.assertRaises(SystemExit):
            play()
        mock_player().warn.assert_called_once_with(f"Invalid solution ABCDE, must be a valid guess")

    @patch('sys.argv', ['test.py', 'AUDIO'])
    @patch('play.CLIPlayer')
    def test_fixed_solution(self, mock_player):
        with self.assertRaises(SystemExit):
            play()
        mock_player().warn.assert_called_once_with(f"Solution will be AUDIO")

    @patch('sys.argv', ['test.py', '--today', '--hints'])
    @patch('play.CLIPlayer')
    def test_today_hints_solution(self, mock_player):
        with self.assertRaises(SystemExit):
            play()
        self.assertEqual(mock_player().GAME_NUMBER, 902)

    @patch('sys.argv', ['test.py', '11'])
    @patch('play.CLIPlayer')
    def test_today_int_solution(self, mock_player):
        with self.assertRaises(SystemExit):
            play()
        self.assertEqual(mock_player().GAME_NUMBER, 11)

    @patch('sys.argv', ['test.py'])
    @patch('random.choice')
    @patch('play.CLIPlayer')
    def test_random_solution(self, mock_player, mock_random):
        mock_player.return_value.again.side_effect = sys.exit
        with self.assertRaises(SystemExit):
            play()
        mock_random.assert_called_once()

    @patch('sys.argv', ['test.py', 'AUDIO'])
    @patch('play.CLIPlayer')
    def test_error1(self, mock_player):
        mock_player.return_value.guess.side_effect = lambda round: "AUDIO"
        mock_player.ASSUME_GUESSES_VALID = True
        mock_player.return_value.handle_win.side_effect = KeyboardInterrupt
        with self.assertRaises(SystemExit):
            play()
        mock_player.return_value.quit.assert_called_with()

    @patch('sys.argv', ['test.py'])
    @patch('play.CLIPlayer')
    def test_error2(self, mock_player):
        mock_player.return_value.guess.side_effect = lambda round: "AUDIO"
        mock_player.ASSUME_GUESSES_VALID = True
        mock_player.return_value.handle_win.side_effect = KeyboardInterrupt
        mock_player.return_value.again.side_effect = KeyboardInterrupt
        with self.assertRaises(SystemExit):
            play()


if __name__ == '__main__':
    unittest.main()
