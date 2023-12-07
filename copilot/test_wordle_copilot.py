import unittest
from wordle import Game, LetterStates

class TestGame(unittest.TestCase):
    def test_check_guess(self):
        solution = "APPLE"
        guess = "APPLE"
        expected = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION]
        self.assertEqual(Game.check_guess(guess, solution), expected)

        guess = "APPLR"
        expected = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.NOTPRESENT]
        self.assertEqual(Game.check_guess(guess, solution), expected)

        guess = "ORANGE"
        expected = [LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT]
        self.assertEqual(Game.check_guess(guess, solution), expected)

    def test_is_same_response(self):
        solution = "APPLE"
        guess = "APPLE"
        response = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION]
        self.assertTrue(Game.is_same_response(guess, solution, response))

        guess = "APPLR"
        response = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.INCORRECTPOSITION]
        self.assertTrue(Game.is_same_response(guess, solution, response))

        guess = "ORANGE"
        response = [LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT, LetterStates.NOTPRESENT]
        self.assertTrue(Game.is_same_response(guess, solution, response))

        guess = "APPLE"
        response = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.INCORRECTPOSITION]
        self.assertFalse(Game.is_same_response(guess, solution, response))

        guess = "ORANGE"
        response = [LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION, LetterStates.CORRECTPOSITION]
        self.assertFalse(Game.is_same_response(guess, solution, response))

if __name__ == '__main__':
    unittest.main()