import Actions
import random
import numpy as np

class DecisionMaker:
    """
    Class implementing the decision-making process for the Multi-Person quizz. Its main method executeRelevantAction
    aims to trigger the most appropriate method of an Action instance of the class Actions, regarding the analysis of
    the NLU (intents, entities,..).
    """

    def __init__(self, multipleChoices, verbose):

        self.multipleChoices = multipleChoices
        self.verbose = verbose

        self.previousAnswer = None
        self.__Action = Actions.Actions(self.multipleChoices)
        self.__questionAsked = False
        self.__currentAnswer0 = None    # Current answer of the player labeled as player 0
        self.__currentAnswer1 = None    # Current answer of the player labeled as player 1
        self.__currentAnswer = "WrongAnswer"
        self.countAnswers = 0
        self.pRandom = 1              # Probability to ask a confirmation for the final answer before checking the
                                        # answer
        self.nbDisagree = 0             # Number of turns where the players disagree on a same question
        self.nbLimitDisagree = 4        # Limit of number of disagreements before proposing to skip the question

        self.previousMsg = None         # Store the latest message sent to the TTS to be able to repeat

    def executeRelevantAction(self, currentUtt: list, person: int) -> (bool, ):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param currentUtt : analysis of the current processed text, list [intent, entity, label]
        :param person: the number which corresponds of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return: onGoing : a boolean which indicates if the game is still running or is ended
        """
        onGoing = True
        previousAct = self.__Action.getPreviousAction()
        msg = ''
        if self.previousMsg is not None:
            if currentUtt[0] == 'repeat_question':
                if self.previousMsg != '':
                    msg = self.__Action.sendTTS(self.previousMsg)
                else:
                    msg = self.__Action.repeatQuestion()
        # if no questions have been asked or if the bot proposed to skip one:
        if (not self.__questionAsked) or (previousAct in ['proposeSkipQ', 'confirm_ans']):
            # If just one player answers when the bot asked if they want to play
            if previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']:
                if (currentUtt[0] == 'agree') or (currentUtt[0] == 'give_answer') : #TODO - Improve this condiiton
                    msg = self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
                elif previousAct == 'proposeSkipQ' and currentUtt[0] == 'disagree':
                    msg = self.__Action.continueSameQuestion()
                elif currentUtt[0] == 'disagree':
                    msg = self.__Action.endQuiz()
                    onGoing = False
            if previousAct == 'confirm_ans':
                if currentUtt[0] == 'agree':
                    msg = self.__Action.checkAnswer(self.__currentAnswer)
                    # Reset the current answer of each person to None
                    self.__currentAnswer0 = None
                    self.__currentAnswer1 = None
                    # Reset the boolean
                    self.__questionAsked = False
                    self.countAnswers = 0
                else:
                    self.countAnswers = 0
                    msg = self.__Action.continueSameQuestion()

        # if a question has been asked : check for agreement
        else:
            # First, handle special cases (clue, ..)
            if previousAct == 'proposeClue':
                # TODO : maybe, allow only one clue per question ?
                if currentUtt[0] == 'agree':
                    msg = self.__Action.giveClue()
                else:
                    msg = self.__Action.continueSameQuestion()
            elif currentUtt[0] == 'ask_clue':
                msg = self.__Action.giveClue()
            elif currentUtt[0] == 'skip_question':
                msg1 = self.__Action.confirm(skip=True)
                msg2 = self.__Action.askQuestion()
                msg = msg1 + ' '+msg2
                self.nbDisagree = 0
            # Otherwise (no special case) :
            # Use the intent to update the current answer of each player to determine if they agree or not
            elif currentUtt[0] == 'give_answer':
                if currentUtt[2][0] is not None:
                    if not self.multipleChoices:
                        # If we don't use multiple choices, update the answer without checking they are in a proposed list
                        self.countAnswers += 1
                        self.previousAnswer = self.__currentAnswer
                        self.__currentAnswer = currentUtt[2][0]
                        msg = self.checkAgreement()

                    else:
                        idx_match = np.array([currentUtt[2][0].casefold() in x.casefold() for x in self.__Action.getQManager().getMultipleChoices()])
                        # Get the index of the list where an element is True (i.e. the entity answer is in an element of the multiple choices)
                        idx_True = np.where(np.array(idx_match)==True)[0]
                        if idx_True.size:
                            # If there is at least one element -> Update the current answer to this element (the first one)
                            self.countAnswers += 1
                            self.previousAnswer = self.__currentAnswer
                            self.__currentAnswer = self.__Action.getQManager().getMultipleChoices()[idx_True[0]]
                            msg = self.checkAgreement()

            elif currentUtt[0] == 'agree' and (previousAct != 'proposeClue'):
                if self.__currentAnswer is not None:
                    if self.multipleChoices and (self.__currentAnswer.casefold() not in [x.casefold() for x in self.__Action.getQManager().getMultipleChoices()]):
                        pass
                    else:
                        p = random.random()
                        if p < self.pRandom:
                            msg = self.__Action.confirm(ans=self.__currentAnswer)
                        else:
                            msg = self.__Action.checkAnswer(self.__currentAnswer)
                            # Reset the current answer of each person to None
                            self.__currentAnswer0 = None
                            self.__currentAnswer1 = None
                            # Reset the boolean
                            self.__questionAsked = False
                            self.countAnswers = 0
                #TODO - Else : Do we need to ask them another country or just wait ?

            elif (currentUtt[0] == 'disagree') and (previousAct != 'proposeClue'):
                self.nbDisagree += 1
                # If too many disagreements, propose to skip a question
                if self.nbDisagree >= self.nbLimitDisagree:
                    msg = self.__Action.proposeClue()
                    self.nbDisagree = 0
        # Verbose for testing
        if self.verbose:
            self.print_vars()
            print(f"Previous act: {previousAct}")
        # Store the message sent to the TTS
        self.previousMsg = msg
        return onGoing, msg

    def checkAgreement(self):
        """
        Check agreement between players - without using the diarization
        :return: msg - the message sent to the TTS (empty if no messages are sent)
        """
        msg = ''
        if self.countAnswers >= 3 and (self.previousAnswer.casefold() == self.__currentAnswer.casefold()):
            p = random.random()
            if p < self.pRandom:
                msg = self.__Action.confirm(ans=self.__currentAnswer)
            else:
                msg = self.__Action.checkAnswer(self.__currentAnswer)
                # Reset the current answer of each person to None
                self.__currentAnswer0 = None
                self.__currentAnswer1 = None
                # Reset the boolean
                self.__questionAsked = False
                self.countAnswers = 0
        elif self.previousAnswer.casefold() != self.__currentAnswer.casefold():
            self.nbDisagree += 1
            # If too many disagreements, propose to skip a question
            if self.nbDisagree >= self.nbLimitDisagree:
                msg = self.__Action.proposeClue()
                self.nbDisagree = 0
        return msg

    # Getters
    def getAction(self):
        return self.__Action

    def getQuestionAsked(self):
        return self.__questionAsked

    def print_vars(self):
        print(
            f"Previous answer: {self.previousAnswer}\n"
            f"Question asked: {self.__questionAsked}\n"
            f"Current answer 0: {self.__currentAnswer0}\n"
            f"Current answer 1: {self.__currentAnswer1}\n"
            f"Current answer : {self.__currentAnswer}\n"
            f"Count answers: {self.countAnswers}\n"
            f"NB Disagree: {self.nbDisagree}\n")
        

if __name__=='__main__':
    DecMaker = DecisionMaker(multipleChoices=True)
    DecMaker.getAction().introduceQuizz()
    DecMaker.executeRelevantAction(['agree', [], []], 0)
    mChoices = DecMaker.getAction().getQManager().getMultipleChoices()
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[0]]], 0)
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[1]]], 1)
    DecMaker.executeRelevantAction(['disagree', [], []], 0)
    DecMaker.executeRelevantAction(['give_answer', ['answer'], [mChoices[2]]], 1)
    DecMaker.executeRelevantAction(['agree', [], []], 0)
