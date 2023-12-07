import subprocess
import unittest
from unittest.mock import MagicMock, call, patch
from cli import CLIConfig, CLIPlayer
from wordle import LetterStates  # Import the class containing the method to test

class TestCLIPlayer(unittest.TestCase):
    def setUp(self):
        self.player = CLIPlayer()

    def test_out(self):
        expected_output = "Test Output"  # Define your expected output string

        # Redirect stdout to capture printed output
        with patch('builtins.print') as mock_stdout:
            self.player.out(expected_output)

            # Check if the expected string was printed
            mock_stdout.assert_called_once_with(f"{expected_output}\x1b[0m\xA0")

    def test_out_empty_string(self):
        # Test the out method with an empty string argument
        with patch('builtins.print') as mock_stdout:
            self.player.out()

            # Check if a non-breaking space was printed
            mock_stdout.assert_called_once_with("\x1b[0m\xA0")

    
    def test_update_keyboard_lines_since_positive(self):
        # Test update_keyboard when _lines_since_keyboard is positive
        self.player._lines_since_keyboard = 2  # Set _lines_since_keyboard to a positive value
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            self.player.update_keyboard()

            # Check if the expected output was written to sys.stdout
            calls = [call("\033[2F"), call("\xA0"), call('\x1b[2E')]
            print(mock_stdout.call_args_list)
            mock_stdout.write.assert_has_calls(calls, any_order=False)

    def test_update_keyboard_lines_since_negative(self):
        # Test update_keyboard when _lines_since_keyboard is -1
        self.player._lines_since_keyboard = -1  # Set _lines_since_keyboard to -1
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            self.player.update_keyboard()

            # Check if the expected output was written to sys.stdout
            mock_stdout.write.assert_called_with("\n")

    def test_handle_loss(self):
        solution = "TestSolution"
        expected_output = f"{self.player._C.LOSE}🤦 LOSE! The solution was {solution}"
        with patch.object(self.player, 'out') as mock_out:
            self.player.handle_loss(solution)

            # Check if the expected output was passed to the out method
            mock_out.assert_called_once_with(expected_output)

    def test_quit(self):
        expected_output = f"{self.player._C.LOSE}QUIT!"
        with patch.object(self.player, 'out') as mock_out:
            self.player.quit()

            # Check if the expected output was passed to the out method
            mock_out.assert_called_once_with(expected_output)

    def test_warn(self):
        warning = "TestWarning"
        expected_output = f"{self.player._C.WARN}{warning}"
        with patch.object(self.player, 'out') as mock_out:
            self.player.warn(warning)

            # Check if the expected output was passed to the out method
            mock_out.assert_called_once_with(expected_output)
    
    @patch('builtins.input', return_value='TestGuess')  # Simulate user input
    @patch('sys.stdout.write')  # Mock sys.stdout.write
    def test_guess(self, mock_stdout_write, mock_input):
        round_number = 1
        expected_prompt = f"Guess {round_number}/6: "
        expected_output = 'TestGuess'

        # Call the guess method
        result = self.player.guess(round_number)

        # Check if the input prompt and stdout.write calls match expectations
        mock_input.assert_called_once_with(expected_prompt)
        mock_stdout_write.assert_called_with('\x1b[A\x1b[11C\x1b[K')

        # Check if the result matches the expected output
        self.assertEqual(result, expected_output.upper())

    @patch.object(CLIPlayer, 'out')  # Mock the out method
    @patch.object(CLIPlayer, 'update_keyboard')  # Mock the update_keyboard method
    def test_start(self, mock_update_keyboard, mock_out):
        # Call the start method
        self.player.start()

        # Check if attributes are initialized correctly
        self.assertEqual(self.player._lines_since_keyboard, -1)
        self.assertEqual(self.player._response_history, [])
        expected_keyboard_status = {letter: LetterStates.NOTGUESSEDYET for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        self.assertDictEqual(self.player._keyboard_status, expected_keyboard_status)

        # Check if the expected output was printed
        mock_out.assert_called_once_with("Let's play a game of Wordle")
        mock_update_keyboard.assert_called_once()
    
    @patch.object(CLIPlayer, 'out')  # Mock the out method
    def test_handle_response(self, mock_out):
        # Initialize keyboard status by calling start method
        self.player.start()
        self.player._keyboard_status['A'] = LetterStates.CORRECTPOSITION
        expected_keyboard_status = self.player._keyboard_status

        guess = "ABC"
        states = [LetterStates.INCORRECTPOSITION, LetterStates.INCORRECTPOSITION, LetterStates.NOTPRESENT]
        hint = 3

        with patch.object(CLIPlayer, 'update_keyboard') as mock_update_keyboard:
            # Call the handle_response method
            self.player.handle_response(guess, states, hint)

            # Check if _response_history is updated correctly
            self.assertEqual(self.player._response_history, [(guess, states)])

            # Check if _keyboard_status is updated correctly
            expected_keyboard_status['A'] = LetterStates.CORRECTPOSITION
            expected_keyboard_status['B'] = LetterStates.INCORRECTPOSITION
            expected_keyboard_status['C'] = LetterStates.NOTPRESENT
            self.assertDictEqual(self.player._keyboard_status, expected_keyboard_status)

            # Check if out and update_keyboard were called with the expected arguments
            expected_out_call = self.player.pretty_response(guess, states, self.player._C) + (f" { self.player._C.DIM }{ hint } possible" if hint != -1 else "")
            mock_out.assert_called_with(expected_out_call)
            mock_update_keyboard.assert_called_once()
    
    @patch('builtins.input', return_value='Play')
    def test_again_play(self, mock_input):
        expected_output = 'Play'

        # Call the again method
        result = self.player.again()

        # Check if input was called with the expected prompt
        mock_input.assert_called_once_with("Play again \x1b[90m[Enter]\x1b[0m or exit \x1b[90m[Ctrl-C]\x1b[0m? ")

        # Check if the result matches the expected output
        self.assertEqual(result, expected_output)
    
    @patch('subprocess.Popen')
    @patch('shutil.which')
    def test_try_clipboard_windows(self, mock_shutil_which, mock_subprocess_popen):
        mock_shutil_which.return_value = "clip.exe"
        mock_subprocess_popen.return_value = MagicMock(returncode=0)
        with patch('platform.uname', return_value=MagicMock(release="microsoft-standard")) as mock_uname:
            with patch('platform.system', return_value="Windows"):
                result = self.player.try_clipboard("Test text")
                mock_shutil_which.assert_called_once_with("clip.exe")
                mock_subprocess_popen.assert_called_once_with("clip.exe", stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, env={'LANG': 'en_US.UTF-8'})
                self.assertTrue(result)

    @patch('subprocess.Popen')
    @patch('shutil.which')
    def test_try_clipboard_linux(self, mock_shutil_which, mock_subprocess_popen):
        mock_shutil_which.return_value = "xclip"
        mock_subprocess_popen.return_value = MagicMock(returncode=0)
        with patch('platform.uname', return_value=MagicMock()):
            with patch('platform.system', return_value="Linux"):
                result = self.player.try_clipboard("Test text")
                mock_shutil_which.assert_called_once_with("xclip")
                mock_subprocess_popen.assert_called_once_with("xclip", stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, env={'LANG': 'en_US.UTF-8'})
                self.assertTrue(result)

    @patch('subprocess.Popen')
    @patch('shutil.which')
    def test_try_clipboard_macos(self, mock_shutil_which, mock_subprocess_popen):
        mock_shutil_which.return_value = "pbcopy"
        mock_subprocess_popen.return_value = MagicMock(returncode=0)
        with patch('platform.uname', return_value=MagicMock()):
            with patch('platform.system', return_value="Darwin"):
                result = self.player.try_clipboard("Test text")
                mock_shutil_which.assert_called_once_with("pbcopy")
                mock_subprocess_popen.assert_called_once_with("pbcopy", stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, env={'LANG': 'en_US.UTF-8'})
                self.assertTrue(result)

    @patch('subprocess.Popen')
    @patch('shutil.which')
    def test_try_clipboard_no_clip_program(self, mock_shutil_which, mock_subprocess_popen):
        mock_shutil_which.return_value = None
        with patch('platform.uname', return_value=MagicMock()):
            with patch('platform.system', return_value="Linux"):
                result = self.player.try_clipboard("Test text")
                mock_shutil_which.assert_called_once_with("xclip")
                mock_subprocess_popen.assert_not_called()
                self.assertFalse(result)

    @patch('cli.CLIPlayer.out')  # Mock the out method
    @patch('cli.CLIPlayer.try_clipboard')  # Mock the try_clipboard method
    def test_handle_win(self, mock_try_clipboard, mock_out):
        round_number = 3  # Set the round number for testing
        # Verify the output messages based on the win conditions
        expected_win_message = f"{self.player._C.WIN}{self.player._C.WIN_MESSAGES[round_number]}! Got it in {round_number}/{6} rounds"

        # Verify the shareable summary content and clipboard copy attempt
        share_text = f"wordle-cli {round_number}/{6}\n"
        share_text += "\n".join("".join(self.player._C.SHARE_EMOJI[state] for state in states) for _, states in self.player._response_history)
        
        # Mock try_clipboard to return True (indicating successful clipboard copying)
        mock_try_clipboard.return_value = True
        self.player.handle_win(round_number)
        mock_try_clipboard.assert_called_with(share_text)
        mock_out.assert_any_call(expected_win_message)
        mock_out.assert_called_with(f"📣 Shareable summary copied to clipboard")


        mock_out.reset_mock()
        # Mock try_clipboard to return False (indicating clipboard copying failed)
        mock_try_clipboard.return_value = False
        self.player.handle_win(round_number)
        mock_try_clipboard.assert_called_with(share_text)

        calls = [call(expected_win_message), call(f"📣 Shareable summary:"), call(f"{share_text}\n")]
        mock_out.assert_has_calls(calls, any_order=False)


if __name__ == '__main__':
    unittest.main()