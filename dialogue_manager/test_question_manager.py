import unittest
import re

import QuestionManager


class TestQuestionManager(unittest.TestCase):

    def test_getCurrentFlag(self):
        self.qm = QuestionManager.QuestionManager()
        self.qm.nextQuestion()

        country = self.qm.getCurrentFlag()
        self.assertTrue(len(country.strip()) > 0)

    def test_getCurrentFlag(self):
        self.qm = QuestionManager.QuestionManager()
        answer: str = self.qm.getCurrentFlag()

        self.assertFalse(answer is None)
        self.assertTrue(re.fullmatch(r'[a-zA-Z\- \']+', answer) is not None)

    def test_getMultipleChoices(self):
        self.qm = QuestionManager.QuestionManager()
        self.qm.nextQuestion()

        options: list = self.qm.getMultipleChoices()
        self.assertTrue(len(options) == 4)

        self.assertTrue(self.qm.getCurrentFlag() in options)


if __name__ == '__main__':
    unittest.main()
