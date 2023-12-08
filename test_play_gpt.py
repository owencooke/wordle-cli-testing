import unittest
from io import StringIO
import sys
from unittest.mock import MagicMock, patch  # Import patch for mocking
from play import play, print_help_exit  # Import your print_help_exit function

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
    @patch('play.print_help_exit', side_effect=sys.exit)
    def test_help_argument(self, mock_help):
        with self.assertRaises(SystemExit):
            play()
        mock_help.assert_called_once_with()

    @patch('sys.argv', ['test.py', '-invalid'])
    @patch('play.print_help_exit', side_effect=sys.exit)
    @patch('play.CLIPlayer')
    def test_invalid_argument(self, mock_player, mock_help):
        with self.assertRaises(SystemExit):
            play()
        mock_player().warn.assert_called_once_with(f"Invalid argument -invalid")
        mock_help.assert_called_once_with()

    @patch('sys.argv', ['test.py', 'ABCDE'])
    @patch('play.print_help_exit', side_effect=sys.exit)
    @patch('play.CLIPlayer')
    def test_invalid_solution(self, mock_player, mock_help):
        with self.assertRaises(SystemExit):
            play()
        mock_player().warn.assert_called_once_with(f"Invalid solution ABCDE, must be a valid guess")
        mock_help.assert_called_once_with()

    @patch('sys.argv', ['test.py', 'AUDIO'])
    @patch('play.CLIPlayer')
    @patch('wordle.Game')
    def test_fixed_solution(self, mock_game, mock_player):
        mock_game_instance = mock_game.return_value  # Get the instance created by the patch
        mock_game_instance.LENGTH = 5 # Set the length of the solution
        mock_game_instance.VALID_GUESSES = ['AUDIO']  # Set the valid guesses
        with self.assertRaises(SystemExit):
            play()
        mock_player().warn.assert_called_once_with(f"Solution will be AUDIO")
        mock_game().play.assert_called_once_with(mock_player(), 'AUDIO', hints=False)

    @patch('sys.argv', ['test.py', '--today', '--hints'])
    @patch('play.CLIPlayer')
    @patch('wordle.Game')
    def test_today_hints_solution(self, mock_game, mock_player):
        mock_game_instance = mock_game.return_value  # Get the instance created by the patch
        mock_game_instance.VALID_SOLUTIONS = ['AUDIO']
        with self.assertRaises(SystemExit):
            play()
        self.assertEqual(mock_player().GAME_NUMBER, 0)
        mock_game().play.assert_called_once_with(mock_player(), 'AUDIO', hints=True)

    @patch('sys.argv', ['test.py', '11'])
    @patch('play.CLIPlayer')
    @patch('wordle.Game')
    def test_today_int_solution(self, mock_game, mock_player):
        mock_game_instance = mock_game.return_value  # Get the instance created by the patch
        mock_game_instance.VALID_SOLUTIONS = ['AUDIO', 'STERN']
        with self.assertRaises(SystemExit):
            play()
        self.assertEqual(mock_player().GAME_NUMBER, 1)
        mock_game().play.assert_called_once_with(mock_player(), 'STERN', hints=False)

    @patch('sys.argv', ['test.py'])
    @patch('random.choice')
    @patch('play.CLIPlayer')
    @patch('wordle.Game')
    def test_random_solution(self, mock_game, mock_player, mock_random):
        mock_game_instance = mock_game.return_value  # Get the instance created by the patch
        mock_game_instance.VALID_SOLUTIONS = ['AUDIO', 'STERN']
        mock_player.return_value.again.side_effect = sys.exit
        with self.assertRaises(SystemExit):
            play()
        mock_game().play.assert_called_once_with(mock_player(), mock_random.return_value, hints=False)
        mock_random.assert_called_once_with(mock_game_instance.VALID_SOLUTIONS)

    @patch('sys.argv', ['test.py'])
    @patch('play.CLIPlayer')
    @patch('wordle.Game')
    def test_errors(self, mock_game, mock_player):
        mock_game_instance = mock_game.return_value  # Get the instance created by the patch
        mock_game_instance.VALID_SOLUTIONS = ['AUDIO', 'STERN']
        mock_game_instance.play.side_effect = KeyboardInterrupt
        mock_player.return_value.again.side_effect = [None, KeyboardInterrupt]
        with self.assertRaises(SystemExit):
            play()
        mock_player.return_value.quit.assert_called_with()


if __name__ == '__main__':
    unittest.main()
