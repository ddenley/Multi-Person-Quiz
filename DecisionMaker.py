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

    def executeRelevantAction(self, currentUtt, lastUtt, nbTexts, i):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param currentUtt
        :param lastUtt
        :param nbTexts
        :param i: the number which correspond of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return:
        """
        # use currentUtt and lastUtt is not None and previous action
        previousAct = self.__Action.getPreviousAction()
        # if no question has been asked :
        if not self.__questionAsked:
            if ((previousAct == 'introQuizz') or (previousAct == 'checkAns')) and (nbTexts == 1):
                if currentUtt[0] == 'agree':
                    self.__Action.askQuestion()
                    self.__questionAsked = True
            elif ((previousAct == 'introQuizz') or (previousAct == 'checkAns')) and (nbTexts == 2):
                if (currentUtt[0] == 'agree') and (i == 1):
                    self.__Action.askQuestion()
                    self.__questionAsked = True
        # if a question has been asked : check for agreement
        else:
            if (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'agree'):
                self.__currentAnswer = lastUtt[1]
                self.__Action.checkAnswer(self.__currentAnswer)
                self.__questionAsked = False
            elif (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'give_answer'):
                if lastUtt[1] == currentUtt[1]:
                    self.__currentAnswer = currentUtt[1]
                    self.__Action.checkAnswer(self.__currentAnswer)
                    self.__questionAsked = False

    def getAction(self):
        return self.__Action

