import Actions
import QuestionManager

class MainDM:
    """
    Main class of the Dialogue Management of the project Multi-Person Quizz.
    This class handle the flow of the information between the STT and the NLU to get the label, intent and the entity for each utterance,
    and trigger the action which seems the most relevant.
    """

    def __init__(self):
        self.__onGoing = True                                   # boolean to indicate if a game is in progress
        self.__questionAsked = False
        # Index to do a test version
        self.idxNTurn = 0
        self.idxNLU = 0

        self.__Action = Actions.Actions()                        # Actions instance
        self.__previousTurns = {'0': [], '1': []}                # dictionary for previous turns for each person
        self.currentLabel = '0'
        self.__currentUtt = ['', '', '']                         # list for current turn [intent, entity, label]
        self.__lastUtt = ['', '', '']                            # list of the previous turn [intent, entity, label]
        self.__currentAnswer = ''                                # current Answer of the participants


    def requestNextTurn(self):
        """
        Request the next turn of the dialogue to the SSR (IBM ASR)
        :return:
        """
        #TODO : Link to the IBM ASR to request the next turn
        #Test version
        texts = ['']                    # list of the text from different people
        labels = ['']                   # list of the labels for each text
        # TEST VERSION HERE
        if self.idxNTurn==0:
            utt = 'Yes, for sure'
            print('-' + utt)
            texts = [utt]
            labels = ['0']
        elif self.idxNTurn==1:
            utt1 = 'Mhmm, I think it is {}, what do you think ?'.format(self.__Action.getQManager().getCurrentFlag())
            utt2 = 'Yes, probably'
            print('-' + utt1)
            print('-' + utt2)
            texts = [utt1, utt2]
            labels = ['0', '1']
        self.nbTexts = len(texts)
        return texts, labels

    def sendAndRequestNLU(self):
        """
        Send the text from the SST to the NLU to get the intent and the entity of this text.
        :return:
        """
        # TODO : Link to Rasa NLU to request the intent + entity of the current text
        intent = ''
        entity = ''
        # TEST VERSION HERE
        if self.idxNTurn==0:
            intent = 'agree'
            entity = ''
        elif self.idxNTurn==1:
            if self.idxNLU==0:
                intent = 'give_answer'
                entity = '{}'.format(self.__Action.getQManager().getCurrentFlag())
            elif self.idxNLU==1:
                intent = 'agree'
                entity = ''
        return intent, entity

    def executeRelevantAction(self, i):
        """
        Choose and execute the action which seems the most relevant regarding the current and previous
        information [intent, entity, label]
        :param i: the number which correspond of the current analysis of the current turn (e.g. is the current turn has
        a text for a first person and a text from the other one, i=0 for the first text and then i=1 for the second)
        :return:
        """
        #use currentUtt and lastUtt is not None and previous action
        previousAct = self.__Action.getPreviousAction()
        # if no question has been asked :
        if not self.__questionAsked:
            if ((previousAct == 'introQuizz') or (previousAct == 'checkAns') ) and (self.nbTexts == 1):
                if self.__currentUtt[0] == 'agree':
                    self.__Action.askQuestion()
                    self.__questionAsked = True
            elif ((previousAct == 'introQuizz') or (previousAct == 'checkAns') ) and (self.nbTexts == 2):
                if (self.__currentUtt[0] == 'agree') and (i == 2):
                    self.__Action.askQuestion()
                    self.__questionAsked = True
        # if a question has been asked : check for agreement
        else:
            if (self.__lastUtt[0] == 'give_answer') and (self.__currentUtt[0] == 'agree'):
                self.__currentAnswer = self.__lastUtt[1]
                self.__Action.checkAnswer(self.__currentAnswer)
                self.__questionAsked = False
            elif (self.__lastUtt[0] == 'give_answer') and (self.__currentUtt[0] == 'give_answer'):
                if self.__lastUtt[1] == self.__currentUtt[1]:
                    self.__currentAnswer = self.__currentUtt[1]
                    self.__Action.checkAnswer(self.__currentAnswer)
                    self.__questionAsked = False

    def main(self):
        """
        Main function to execute to handle the dialogue
        :return:
        """
        self.__Action.introduceQuizz()
        while self.__onGoing and self.idxNTurn<2:
            # Get the next Turn (transcription of speech to text with label from ASR)
            texts, labels = self.requestNextTurn()
            self.idxNLU = 0
            for i in range(len(texts)):
                # For each text, get the analysis of it from Rasa NLU (i.e. intent + entity) and update the currentUtt
                self.__currentUtt[0], self.__currentUtt[1] = self.sendAndRequestNLU()
                self.__currentUtt[2] = labels[i]
                # Execute the relevant action regarding the NLU response
                self.executeRelevantAction(i+1)
                # Update the last Utt
                self.__lastUtt[0], self.__lastUtt[1], self.__lastUtt[2] = self.__currentUtt[0], self.__currentUtt[1], self.__currentUtt[2]
                self.idxNLU +=1
            self.idxNTurn +=1


if __name__=='__main__':
    DM = MainDM()
    DM.main()