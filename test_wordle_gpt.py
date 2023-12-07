import unittest
from unittest.mock import MagicMock, patch
from wordle import Game, LetterStates

count = 0

def mock_guess(number):
    # Define a mapping of numbers to strings
    number_to_string = {
        1: "STERN",
        2: "HAUNT",
        3: "AUDIO",
    }
    
    # Return the corresponding string if the number is in the mapping
    return number_to_string.get(number, "Unknown")

def mock_guess2(number):
    number_to_string = {
        1: "STERN"
    }
    return number_to_string.get(number, "Unknown")

def mock_guess3(number):
    global count
    number_to_string = {
        1: "AUDIOY" if count == 0 else "ABCDE"
    }
    if count == 2:
        number_to_string[1] = "AUDIO"
    count += 1
    return number_to_string.get(number, "Unknown")

class TestWordle(unittest.TestCase):
    def test_check_equal_guess_and_solution(self):
        guess = "ABCDE"
        solution = "ABCDE"
        result = Game.check_guess(guess, solution)
        self.assertEqual(result, [LetterStates.CORRECTPOSITION] * len(guess))

    def test_check_all_incorrect_positions(self):
        guess = "ABCDE"
        solution = "EABCD"
        result = Game.check_guess(guess, solution)
        self.assertEqual(result, [LetterStates.INCORRECTPOSITION] * len(guess))

    def test_check_all_not_present(self):
        guess = "ABCDE"
        solution = "FGHIJ"
        result = Game.check_guess(guess, solution)
        self.assertEqual(result, [LetterStates.NOTPRESENT] * len(guess))

    def test_check_combination_of_positions(self):
        guess = "ABCDE"
        solution = "ACFCB"
        result = Game.check_guess(guess, solution)
        expected = [
            LetterStates.CORRECTPOSITION,  # A - correct position
            LetterStates.INCORRECTPOSITION,       # B - not in solution
            LetterStates.INCORRECTPOSITION,  # C - correct position
            LetterStates.NOTPRESENT,# D - incorrect position
            LetterStates.NOTPRESENT        # E - not in solution
        ]
        self.assertEqual(result, expected)

    def test_no_matches(self):
        guess = "ABCDE"
        solution = "ZYXWV"
        result = Game.check_guess(guess, solution)
        self.assertEqual(result, [LetterStates.NOTPRESENT] * len(guess))

    def test_same_guess_and_solution(self):
        guess = "ABCDE"
        solution = "ABCDE"
        response = [LetterStates.CORRECTPOSITION] * len(guess)
        result = Game.is_same_response(guess, solution, response)
        self.assertTrue(result)

    def test_different_guess_and_solution(self):
        guess = "ABCDE"
        solution = "EABCD"
        response = [LetterStates.INCORRECTPOSITION] * len(guess)
        result = Game.is_same_response(guess, solution, response)
        self.assertTrue(result)

    def test_mismatched_response(self):
        guess = "ABCDE"
        solution = "FGHIJ"
        response = [LetterStates.NOTPRESENT] * len(guess)
        result = Game.is_same_response(guess, solution, response)
        self.assertTrue(result)

    def test_combination_of_positions(self):
        guess = "ABCDE"
        solution = "ACFDB"
        response = [
            LetterStates.CORRECTPOSITION,  # A - correct position
            LetterStates.INCORRECTPOSITION,       # B - not in solution
            LetterStates.INCORRECTPOSITION,  # C - correct position
            LetterStates.CORRECTPOSITION,# D - incorrect position
            LetterStates.NOTPRESENT        # E - not in solution
        ]
        result = Game.is_same_response(guess, solution, response)
        self.assertTrue(result)

    def test_false_with_wrong_response(self):
        guess = "ABCDE"
        solution = "ACFCB"
        response = [
            LetterStates.CORRECTPOSITION,  # A - correct position
            LetterStates.NOTPRESENT,       # B - not in solution
            LetterStates.CORRECTPOSITION,  # C - correct position
            LetterStates.NOTPRESENT,       # D - not in solution (should be INCORRECTPOSITION)
            LetterStates.NOTPRESENT        # E - not in solution
        ]
        result = Game.is_same_response(guess, solution, response)
        self.assertFalse(result)

    def test_wrong_state_not_present(self):
        guess = "ABCDE"
        solution = "ACFDB"
        response = [
            LetterStates.NOTPRESENT,  # A - correct position
            LetterStates.INCORRECTPOSITION,       # B - not in solution
            LetterStates.INCORRECTPOSITION,  # C - correct position
            LetterStates.CORRECTPOSITION,  # D - incorrect position (should be INCORRECTPOSITION)
            LetterStates.NOTPRESENT        # E - not in solution
        ]
        result = Game.is_same_response(guess, solution, response)
        self.assertFalse(result)
    
    def test_wrong_state_correct(self):
        guess = "ABCDE"
        solution = "ACFDB"
        response = [
            LetterStates.CORRECTPOSITION,  # A - correct position
            LetterStates.INCORRECTPOSITION,       # B - not in solution
            LetterStates.INCORRECTPOSITION,  # C - correct position
            LetterStates.CORRECTPOSITION,  # D - incorrect position (should be INCORRECTPOSITION)
            LetterStates.CORRECTPOSITION        # E - not in solution
        ]
        result = Game.is_same_response(guess, solution, response)
        self.assertFalse(result)

    @patch('sys.stdout.write')
    def test_play(self, mock_stdout_write):
        # Mocking external modules, player, and their methods
        player_mock = MagicMock()
        player_mock.ASSUME_GUESSES_VALID = False
        player_mock.guess = mock_guess
        player_mock.handle_response.side_effect = [None] * 6

        # Simulated solution
        solution = "AUDIO"

        # Simulate the game
        game = Game()
        result = game.play(player_mock, solution, True)

        # Assertions for the expected behavior of the game loop
        self.assertEqual(result, 3)  # Expected round at which the win occurred
        # Additional assertions as needed for method calls, mocks, etc.

    @patch('sys.stdout.write')
    def test_loss(self, mock_stdout_write):
        # Mocking external modules, player, and their methods
        player_mock = MagicMock()
        player_mock.ASSUME_GUESSES_VALID = True
        player_mock.guess = mock_guess2
        player_mock.handle_loss = MagicMock()
        player_mock.handle_response.side_effect = [None] * 6

        # Simulated solution
        solution = "AUDIO"

        # Simulate the game
        game = Game()
        game.ROUNDS = 1
        result = game.play(player_mock, solution)

        # Assertions for the expected behavior of the game loop
        self.assertIsNone(result)  # Expected round at which the win occurred

    @patch('sys.stdout.write')
    def test_play_long(self, mock_stdout_write):
        # Mocking external modules, player, and their methods
        player_mock = MagicMock()
        player_mock.ASSUME_GUESSES_VALID = False
        player_mock.guess = mock_guess3
        player_mock.handle_response.side_effect = [None] * 6

        # Simulated solution
        solution = "AUDIO"

        # Simulate the game
        game = Game()
        result = game.play(player_mock, solution, False)

        # Assertions for the expected behavior of the game loop
        self.assertEqual(result, 1)  # Expected round at which the win occurred
        # Additional assertions as needed for method calls, mocks, etc.


if __name__ == "__main__":
    unittest.main()
