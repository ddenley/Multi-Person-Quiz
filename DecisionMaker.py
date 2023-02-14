import Actions


class DecisionMaker:
    """
    Class implementing the decision-making process for the Multi-Person quizz. Its main method executeRelevantAction
    aims to trigger the most appropriate method of an Action instance of the class Actions, regarding the analysis of
    the NLU (intents, entities,..).
    """

    def __init__(self):
        self.__Action = Actions.Actions()
        self.__questionAsked = False
        self.__currentAnswer = None
        self.nbDisagree = 0                         # Number of turns where the players disagree on a same question
        self.nbLimitDisagree = 3                    # Limit of number of disagreement before propose to skip the question

    def executeRelevantAction(self, currentUtt, lastUtt, nbTexts, i):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param currentUtt : analysis of the current processed text, list [intent, entity, label]
        :param lastUtt : analysis of the previous processed text, list [intent, entity, label]
        :param nbTexts : number of texts in the current turn (typically 1 if just 1 of the players talks)
        :param i: the number which correspond of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return: trigger the most appropriate action
        """
        previousAct = self.__Action.getPreviousAction()
        # if no questions has been asked :
        if (not self.__questionAsked) or (previousAct == 'proposeSkipQ'):
            if (previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']) and (nbTexts == 1):
                if currentUtt[0] == 'agree':
                    self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
            elif (previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']) and (nbTexts == 2):
                if ((currentUtt[0] == 'agree') and (lastUtt[0] == 'agree')) and (i == 1):
                    self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
        # if a question has been asked : check for agreement
        else:
            if currentUtt[0] == 'repeat':
                self.__Action.repeatQuestion()
            elif (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'agree'):
                self.__currentAnswer = lastUtt[1]
                self.__Action.checkAnswer(self.__currentAnswer)
                self.__questionAsked = False
            elif (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'give_answer'):
                if lastUtt[1] == currentUtt[1]:
                    self.__currentAnswer = currentUtt[1]
                    self.__Action.checkAnswer(self.__currentAnswer)
                    self.__questionAsked = False
                else:
                    # Disagreement between the players
                    self.__currentAnswer = currentUtt[1]    # Update the current answer
                    self.nbDisagree += 1
                    # If too many disagreements, propose to skip a question
                    if self.nbDisagree >= self.nbLimitDisagree:
                        self.__Action.proposeSkipQuestions()
            elif (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'disagree'):
                # Disagreement between the players
                self.nbDisagree += 1
                # If too many disagreements, propose to skip a question
                if self.nbDisagree >= self.nbLimitDisagree:
                    self.__Action.proposeSkipQuestions()


    # Getters
    def getAction(self):
        return self.__Action

