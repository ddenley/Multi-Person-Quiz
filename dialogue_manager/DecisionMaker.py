import Actions
import random

class DecisionMaker:
    """
    Class implementing the decision-making process for the Multi-Person quizz. Its main method executeRelevantAction
    aims to trigger the most appropriate method of an Action instance of the class Actions, regarding the analysis of
    the NLU (intents, entities,..).
    """

    def __init__(self):
        self.__Action = Actions.Actions()
        self.__questionAsked = False
        self.__currentAnswer0 = None    # Current answer of the player labeled as player 0
        self.__currentAnswer1 = None    # Current answer of the player labeled as player 1
        self.__currentAnswer = None
        self.pRandom = 0.4              # Probability to ask a confirmation for the final answer before checking the
                                        # answer
        self.nbDisagree = 0             # Number of turns where the players disagree on a same question
        self.nbLimitDisagree = 5        # Limit of number of disagreements before proposing to skip the question

    def executeRelevantAction(self, currentUtt: list, lastUtt: list, nbTexts: int, person: int) -> (bool, ):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param currentUtt : analysis of the current processed text, list [intent, entity, label]
        :param lastUtt : analysis of the previous processed text, list [intent, entity, label]
        :param nbTexts : number of texts in the current turn (typically 1 if just 1 of the players talks)
        :param person: the number which corresponds of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return: onGoing : a boolean which indicates if the game is still running or is ended
        """
        onGoing = True
        previousAct = self.__Action.getPreviousAction()
        msg = ''
        # if no questions have been asked or if the bot proposed to skip one:
        if (not self.__questionAsked) or (previousAct in ['proposeSkipQ', 'confirm_ans']):
            # If just one player answers when the bot asked if they want to play
            if previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']:
                if (currentUtt[0] == 'yes') or (currentUtt[0] == 'agree') or (currentUtt[0] == 'give_answer') : #TODO - Improve this condiiton
                    msg = self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
                elif previousAct == 'proposeSkipQ' and currentUtt[0] == 'no':
                    msg = self.__Action.continueSameQuestion()
                elif currentUtt[0] == 'no':
                    msg = self.__Action.endQuiz()
                    onGoing = False
            if previousAct == 'confirm_ans':
                if currentUtt[0] == 'yes':
                    msg = self.__Action.checkAnswer(self.__currentAnswer)
                    self.__questionAsked = False

        # if a question has been asked : check for agreement
        else:
            # First, handle special cases (clue, ..)
            if previousAct == 'proposeClue':
                # TODO : maybe, allow only one clue per question ?
                if currentUtt[0] == 'yes':
                    msg = self.__Action.giveClue()
                else:
                    msg = self.__Action.continueSameQuestion()
            elif currentUtt[0] == 'ask_clue':
                msg = self.__Action.giveClue()
            elif currentUtt[0] == 'skip_question':
                msg1 = self.__Action.confirm(skip=True)
                msg2 = self.__Action.askQuestion()
                msg = msg1 + ' ' +msg2
                self.nbDisagree = 0
            elif currentUtt[0] == 'repeat_question':
                msg = self.__Action.repeatQuestion()
            # Otherwise (no special case) :
            # Use the intent to update the current answer of each player to determine if they agree or not
            elif currentUtt[0] == 'give_answer':
                # Update the current answer of the player 0 if its answer is in the MultipleChoices
                if currentUtt[2][0] in self.__Action.getQManager().getMultipleChoices():
                    if person == 0:
                        self.__currentAnswer0 = currentUtt[2][0]
                    else:
                        self.__currentAnswer1 = currentUtt[2][0]
                # Check if disagreement or agreement
                if (self.__currentAnswer1 is not None) and (self.__currentAnswer0 is not None) and (self.__currentAnswer0 != self.__currentAnswer1):
                    self.nbDisagree += 1
                    # If too many disagreements, propose to skip a question
                    if self.nbDisagree >= self.nbLimitDisagree:
                        msg = self.__Action.proposeClue()
                elif (self.__currentAnswer1 is not None) and (self.__currentAnswer0 is not None) and (self.__currentAnswer0 == self.__currentAnswer1):
                    # Agreement : ask a confirmation with a probability of pRandom
                    self.__currentAnswer = self.__currentAnswer0
                    p = random.random()
                    if p < self.pRandom:
                        msg = self.__Action.confirm(ans=self.__currentAnswer)
                    else:
                        msg = self.__Action.checkAnswer(self.__currentAnswer0)
                        self.__questionAsked = False
            elif currentUtt[0] == 'agree':
                if (person == 0) and (self.__currentAnswer1 is not None):
                    msg = self.__Action.checkAnswer(self.__currentAnswer1)
                    self.__questionAsked = False
                elif (person == 1) and (self.__currentAnswer0 is not None):
                    msg = self.__Action.checkAnswer(self.__currentAnswer0)
                    self.__questionAsked = False
            elif currentUtt[0] == 'disagree':
                self.nbDisagree += 1
                # If too many disagreements, propose to skip a question
                if self.nbDisagree >= self.nbLimitDisagree:
                    msg = self.__Action.proposeClue()
        return onGoing, msg

    # Getters
    def getAction(self):
        return self.__Action

    def getQuestionAsked(self):
        return self.__questionAsked

if __name__=='__main__':
    DecMaker = DecisionMaker()
    DecMaker.getAction().introduceQuizz()
    DecMaker.executeRelevantAction(['agree', [], []], [], 1, 0)
    mChoices = DecMaker.getAction().getQManager().getMultipleChoices()
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[0]]], [], 1, 0)
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[1]]], [], 1, 1)
    DecMaker.executeRelevantAction(['disagree', [], []], [], 1, 0)
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[2]]], [], 1, 1)
    DecMaker.executeRelevantAction(['agree', [], []], [], 1, 0)