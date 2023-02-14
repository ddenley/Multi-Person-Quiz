import DecisionMaker

class MainDM:
    """
    Main class of the Dialogue Management of the project Multi-Person Quizz.
    This class handle the flow of the information between the STT and the NLU to get the label, intent and the entity for each utterance,
    and trigger the action which seems the most relevant using the DecisionMaker class.
    """

    def __init__(self):
        self.__onGoing = True                                   # boolean to indicate if a game is in progress

        # Index to do a test version
        self.idxNTurn = 0
        self.idxNLU = 0

        self.__DecisionMaker = DecisionMaker.DecisionMaker()     # DecisionMaker instance

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
            utt1 = 'Mhmm, I think it is {}, what do you think ?'.format(self.__DecisionMaker.getAction().getQManager().getCurrentFlag())
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
                entity = '{}'.format(self.__DecisionMaker.getAction().getQManager().getCurrentFlag())
            elif self.idxNLU==1:
                intent = 'agree'
                entity = ''
        return intent, entity

    def main(self):
        """
        Main function to execute to handle the dialogue
        :return:
        """
        self.__DecisionMaker.getAction().introduceQuizz()
        while self.__onGoing and self.idxNTurn<2:
            # Get the next Turn (transcription of speech to text with label from ASR)
            texts, labels = self.requestNextTurn()
            self.idxNLU = 0
            for i in range(len(texts)):
                # For each text, get the analysis of it from Rasa NLU (i.e. intent + entity) and update the currentUtt
                self.__currentUtt[0], self.__currentUtt[1] = self.sendAndRequestNLU()
                self.__currentUtt[2] = labels[i]
                # Execute the relevant action regarding the NLU response
                self.__DecisionMaker.executeRelevantAction(self.__currentUtt, self.__lastUtt, self.nbTexts, i)
                # Update the last Utt
                self.__lastUtt[0], self.__lastUtt[1], self.__lastUtt[2] = self.__currentUtt[0], self.__currentUtt[1], self.__currentUtt[2]
                self.idxNLU +=1
            self.idxNTurn +=1


if __name__=='__main__':
    DM = MainDM()
    DM.main()