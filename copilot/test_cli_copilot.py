import unittest
from unittest.mock import patch
from wordle import LetterStates
from cli import CLIConfig, CLIPlayer

class TestCLIPlayer(unittest.TestCase):
    def setUp(self):
        self.player = CLIPlayer()

    def test_guess(self):
        with patch('builtins.input', return_value='APPLE'):
            guess = self.player.guess(1)
            self.assertEqual(guess, 'APPLE')

    def test_handle_response(self):
        guess = 'APPLE'
        states = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION]
        hint = 2
        expected_response_history = [(guess, states)]
        expected_keyboard_status = {'A': LetterStates.CORRECTPOSITION, 'P': LetterStates.CORRECTPOSITION, 'L': LetterStates.CORRECTPOSITION, 'E': LetterStates.CORRECTPOSITION, 'R': LetterStates.CORRECTPOSITION}
        
        self.player.handle_response(guess, states, hint)
        self.assertEqual(self.player._response_history, expected_response_history)
        self.assertEqual(self.player._keyboard_status, expected_keyboard_status)

    def test_pretty_response(self):
        word = 'APPLE'
        states = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION]
        config = CLIConfig()
        expected_output = '\033[92mA\033[0m\033[92mP\033[0m\033[92mP\033[0m\033[92mL\033[0m\033[92mE\033[0m'
        
        output = CLIPlayer.pretty_response(word, states, config)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()