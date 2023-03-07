# Author:       Andy Edmondson
# Date:         27 Feb 2023
# Purpose:      Test the MainDM class methods
# ---------
# Uses mock to set the data for various functions such as:
#       self.__Action.getPreviousAction()
#       connection_manager.tts_post()
#       connection_manager.gui_post()

import unittest
from unittest.mock import Mock, patch

import DecisionMaker
import connection_manager


class MyTestCase(unittest.TestCase):

    @patch('connection_manager.gui_post')
    @patch('connection_manager.tts_post')
    @patch('Actions.Actions.getPreviousAction', side_effect=['introQuizz', 'checkAns', 'proposeSkipQ', 'proposeSkipQ',
                                                             'introQuizz', 'checkAns', 'proposeSkipQ', 'proposeSkipQ'])
    def test_executeRelevantAction_want_question(self, mock_request, mock_tts, mock_gui):
        """Check that a question is asked when:
         - a question has not already been asked AND
         - previous act is one of ['introQuizz', 'checkAns', 'proposeSkipQ'] AND
         - nbTexts is 1 or 2 AND
         - current utterance intent is 'concur'."""

        # Have the APIs return success.
        mock_tts.return_value = 200
        mock_gui.return_value = 200

        dm = DecisionMaker.DecisionMaker()

        current_utt = ['concur', 'agree', 'yes']
        previous_utt = ['concur', 'agree', 'yes']

        res = dm.executeRelevantAction(current_utt, previous_utt, 1, 1)
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        dm.__init__()

        res = dm.executeRelevantAction(current_utt, previous_utt, 1, 1)
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        res = dm.executeRelevantAction(current_utt, previous_utt, 1, 1)     # Test line 32 part b
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        dm.__init__()

        current_utt = ['NOTconcur', 'agree', 'yes']    #

        res = dm.executeRelevantAction(current_utt, previous_utt, 1, 1)     # Test line 39
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        dm.__init__()

        current_utt = ['concur', 'agree', 'yes']

        res = dm.executeRelevantAction(current_utt, previous_utt, 2, 1)     # Test line 47
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        dm.__init__()

        res = dm.executeRelevantAction(current_utt, previous_utt, 2, 1)     # Test line 47
        self.assertTrue(res)
        self.assertTrue(dm.getQuestionAsked())

        dm.__init__()

        current_utt = ['NOTconcur', 'agree', 'yes']
        previous_utt = ['NOTconcur', 'agree', 'yes']

        res = dm.executeRelevantAction(current_utt, previous_utt, 2, 1)     #
        self.assertTrue(res)
        self.assertFalse(dm.getQuestionAsked())

        dm.__init__()

        current_utt = ['NOTconcur', 'agree', 'yes']
        previous_utt = ['concur', 'agree', 'yes']

        res = dm.executeRelevantAction(current_utt, previous_utt, 2, 1)     # Test line 52 - should stop
        self.assertFalse(res)
        self.assertFalse(dm.getQuestionAsked())


if __name__ == '__main__':
    unittest.main()
