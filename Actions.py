import QuestionManager

class Actions:
    """
    Gather the main actions for the bot for the Multi-Person Quizz, and the methods to send the output message to the
    TTS and the GUI.
    # TODO : Add a repository of different ways to says each message to introduce random message with the same meaning
    """

    def __init__(self):
        """
        Constructor of the class Actions, instantiation of the QuestionManager class
        """
        self.__previousAction = None
        self.__QManager = QuestionManager.QuestionManager()

    def sendTTS(self, msg):
        """
        Send the message from the bot to the TTS to display the text to the users.
        :param msg: message to send
        :return:
        """
        #TODO : Link to the TTS -> send to the TTS
        print('----' * 10)
        print('-' + msg)
        print('----'*10)
        pass

    def sendGUI(self, img_path):
        """
        Send the path of the image and the multiple choices to the GUI.
        :param img_path:
        :return:
        """
        # TODO : Link to the GUI -> send to the GUI
        #print(img_path)
        pass

    def introduceQuizz(self):
        """
        Introduce the quizz to the players.
        :return:
        """
        self.sendTTS("Hey! Would you like to play a game ? You must associate each flag with its country.")
        self.__previousAction = 'introQuizz'

    def askQuestion(self):
        """
        Ask a question to the players.
        :return:
        """
        msg = 'What is this flag ?'
        img_path = 'image path'
        self.sendTTS(msg)
        self.sendGUI(img_path)
        self.__previousAction = 'askQuestion'
        self.__QManager.nextQuestion()
        choices = self.__QManager.getMultipleChoices()
        for i in range(len(choices)):
            print('{} : {}'.format(i, choices[i]))
        self.__QManager.displayFlag()

    def repeatQuestion(self):
        pass

    def checkAgreement(self):
        #NB : This methode seems to be replaced by the methode executeRelevantAction of MainDM class
        pass

    def checkAnswer(self, ans):
        """
        Check the answer of the players and propose a new game.
        :param ans: answer of the players.
        :return:
        """
        self.__previousAction = 'checkAns'
        if ans == self.__QManager.getCurrentFlag():
            self.__QManager.nbSuccess += 1
            self.sendTTS("Well done, it's right ! Would you like to continue to play ?")
            return
        else:
            self.sendTTS("Unfortunately it's not the right answer. This is the flag of {} ! Would you like to try another flag ?".format(self.__QManager.getCurrentFlag()))

    def engagePlayers(self):
        # TODO : How to engage the discussion between the payers, To be continued
        pass

    def skipQuestions(self):

         # TODO : skip question
        pass

    def paraphraseMessage(self, meaning):
        pass

    # Getters
    def getPreviousAction(self):
        return self.__previousAction

    def getQManager(self):
        return self.__QManager