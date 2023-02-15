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
        self.nbLimitDisagree = 3                    # Limit of number of disagreements before proposing to skip the question

    def executeRelevantAction(self, currentUtt, lastUtt, nbTexts, i):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param currentUtt : analysis of the current processed text, list [intent, entity, label]
        :param lastUtt : analysis of the previous processed text, list [intent, entity, label]
        :param nbTexts : number of texts in the current turn (typically 1 if just 1 of the players talks)
        :param i: the number which corresponds of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return: onGoing : a boolean which indicates if the game is still running or is ended
        """
        onGoing = True
        previousAct = self.__Action.getPreviousAction()
        # if no questions have been asked or if the bot proposed to skip one:
        if (not self.__questionAsked) or (previousAct == 'proposeSkipQ'):
            # If just one player answers when the bot asked if they want to play
            if (previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']) and (nbTexts == 1):
                if currentUtt[0] == 'agree':
                    self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
                elif previousAct == 'proposeSkipQ' and currentUtt[0] == 'disagree':
                    self.__Action.continueSameQuestion()
                elif currentUtt[0] == 'disagree':
                    self.__Action.endQuiz()
                    onGoing = False
            # If two players answer when the bot asked if they want to play
            elif (previousAct in ['introQuizz', 'checkAns', 'proposeSkipQ']) and (nbTexts == 2):
                # If they agree to play
                if ((currentUtt[0] == 'agree') and (lastUtt[0] == 'agree')) and (i == 1):
                    self.__Action.askQuestion()
                    self.__questionAsked = True
                    self.nbDisagree = 0
                # If they disagree (i.e. one wants to play but not the other)
                elif (currentUtt[0] != lastUtt[0]) and (i == 1):
                    self.__Action.endQuiz(pDisagree=True)
                    onGoing = False

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
                        self.__Action.proposeSkipQuestion()
            elif (lastUtt[0] == 'give_answer') and (currentUtt[0] == 'disagree'):
                # Disagreement between the players
                self.nbDisagree += 1
                # If too many disagreements, propose to skip a question (we can probably add a probability to ask to
                # skip in order to be more flexible)
                if self.nbDisagree >= self.nbLimitDisagree:
                    self.__Action.proposeSkipQuestion()
        return onGoing


    # Getters
    def getAction(self):
        return self.__Action

