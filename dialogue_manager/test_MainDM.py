# Author:       Andy Edmondson
# Date:         27 Feb 2023
# Purpose:      Test the MainDM class methods
# ---------
# Uses mock to emulate the API calls to other modules.


import unittest
from unittest.mock import patch

from dialogue_manager.MainDM import MainDM

# Using methods from:
# https://docs.python.org/3/library/unittest.mock.html
# https://realpython.com/testing-third-party-apis-with-mocks/


class TestQuestionManager(unittest.TestCase):
    @patch('connection_manager.rasa_nlu_post')
    def test_sendAndRequestNLU_simple(self, mock_request):
        """Test a basic expected rasa return. Server returns are mocked."""

        dm = MainDM()

        intents_json = {
            'text': "Sure, let's guess Malaysia.",
            'intent':
            {
                'name': 'give_answer',
                'confidence': 0.9895011782646179
            },
            'entities':
            [
                {
                    'entity': 'answer',
                    'start': 18,
                    'end': 26,
                    'confidence_entity': 0.9995859265327454,
                    'value': 'Malaysia',
                    'extractor': 'DIETClassifier'
                }
            ],
            'text_tokens': [[0, 4], [6, 9], [10, 11], [12, 17], [18, 26]],
            'intent_ranking':
            [
                {'name': 'give_answer','confidence': 0.9895011782646179},
                {'name': 'greet','confidence': 0.010290027596056461},
                {'name': 'goodbye', 'confidence': 0.0001419934123987332},
                {'name': 'concur', 'confidence': 6.475452391896397e-05},
                {'name': 'contest', 'confidence': 1.9672743292176165e-06}
            ]
            }

        mock_request.return_value.json.return_value = intents_json

        info = dm.sendAndRequestNLU("Sure, let's guess Malaysia.", "some_id")
        expected = ['give_answer', ['answer', 'Malaysia']]
        self.assertEqual(expected, info)

    @patch('connection_manager.rasa_nlu_post')
    def test_sendAndRequestNLU_multi_entity(self, mock_request):
        """Test a basic expected rasa return with multiple entities. Server returns are mocked."""

        dm = MainDM()

        intents_json = {
            'text': "Sure, let's guess Malaysia.",
            'intent':
            {
                'name': 'give_answer',
                'confidence': 0.9895011782646179
            },
            'entities':
            [
                {
                    'entity': 'answer',
                    'start': 18,
                    'end': 26,
                    'confidence_entity': 0.9995859265327454,
                    'value': 'Malaysia',
                    'extractor': 'DIETClassifier'
                },
                {
                    'entity': 'answer',
                    'start': 18,
                    'end': 26,
                    'confidence_entity': 0.9995859265327454,
                    'value': 'Belize',
                    'extractor': 'DIETClassifier'
                }
            ],
            'text_tokens': [[0, 4], [6, 9], [10, 11], [12, 17], [18, 26]],
            'intent_ranking':
            [
                {'name': 'give_answer','confidence': 0.9895011782646179},
                {'name': 'greet','confidence': 0.010290027596056461},
                {'name': 'goodbye', 'confidence': 0.0001419934123987332},
                {'name': 'concur', 'confidence': 6.475452391896397e-05},
                {'name': 'contest', 'confidence': 1.9672743292176165e-06}
            ]
            }

        mock_request.return_value.json.return_value = intents_json

        info = dm.sendAndRequestNLU("Sure, let's guess Malaysia.", "some_id")
        expected = ['give_answer', [['answer', 'Malaysia'], ['answer', 'Belize']]]
        self.assertEqual(expected, info)

    @patch('connection_manager.stt_get')
    def test_getTurnBatch_200(self, mock_request):
        """200 code giving a full batch. Server returns from the STT module are mocked."""

        dm = MainDM()

        return_val1 = ["test text 1", 1, 200]
        mock_request.return_value = return_val1

        # Batch of 5 in this case
        actual_value = dm.get_turn_batch(5)
        expected_value = [return_val1] * 5

        self.assertEqual(expected_value, actual_value)

    # https://stackoverflow.com/questions/24897145/python-mock-multiple-return-values
    @patch('connection_manager.stt_get', side_effect=[["test text 1", 1, 200], [None, None, 204]])
    def test_getTurnBatch_204(self, mock_request):
        """204 code interrupting the batch."""

        dm = MainDM()

        # Batch of 5 in this case, should only return 2 lists instead of a full batch.
        actual_value = dm.get_turn_batch(5)
        expected_value = [["test text 1", 1, 200], [None, None, 204]]

        self.assertEqual(expected_value, actual_value)


if __name__ == '__main__':
    unittest.main()
