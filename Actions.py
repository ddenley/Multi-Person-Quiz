import QuestionManager
import connection_manager as cm


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
        code = cm.tts_post(msg)
        # Print for debug
        print('- ', msg)
        # TODO - Error checks

    def sendGUI(self, img_path):
        """
        Send the path of the image and the multiple choices to the GUI.
        :param img_path:
        :return:
        """
        code = cm.gui_post(img_path)
        # TODO - Error checks

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
        # TODO :  Improve the message to send to the TTS
        msg = 'What is this flag ?'
        img_path = 'static/data/flagImg/st.png'
        self.sendTTS(msg)
        self.sendGUI(img_path)
        self.__previousAction = 'askQuestion'
        self.__QManager.nextQuestion()
        choices = self.__QManager.getMultipleChoices()
        for i in range(len(choices)):
            self.sendTTS('{} : {}'.format(i, choices[i])) # to be adapted with the way to send to the TTS the multiple choices
        # display the flag with matplotlib.pyplot just for test but to be removed when it'll integrate with GUI
        #self.__QManager.displayFlag()

    def repeatQuestion(self):
        """
        Repeat the current question
        :return:
        """
        self.sendTTS('Absolutely, I can repeat the different choices.')
        # TODO : to be adapted with the way to send the message to the TTS
        choices = self.__QManager.getMultipleChoices()
        for i in range(len(choices)):
            self.sendTTS('{} : {}'.format(i, choices[i]))


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
            self.sendTTS("Unfortunately it's not the right answer. This is the flag of {} ! Would you like to try "
                         "another flag ?".format(self.__QManager.getCurrentFlag()))

    def ask_finalAnswer(self, ans):
        self.sendTTS("So, is {} your final answer ?".format(ans))
        self.__previousAction = 'ask_finalAnswer'

    def engagePlayers(self):
        # TODO : How to engage the discussion between the payers, To be continued
        pass

    def endQuiz(self, pDisagree = False):
        """
        End of the quiz (i.e. the players asked to quit or say no when the bot asked if they want to continue)
        :param pDisagree : boolean which indicates if just one of the player doesn't want to continue/to play
        """
        if pDisagree:
            self.sendTTS("It seems that one of the player doesn't want to play. You need to be two in order to "
                         "discuss together. Please come again when all of the players want to play")
        else:
            self.sendTTS('I understand, see you later !')
        # Should the bot display the results of the quiz ?! (i.e. number/percentage of successes)

    def continueSameQuestion(self):
        """
        Continue on the same question when the bot asked previously if the players want to skip a question
        """
        self.sendTTS('No problem, keep going on this question !')
        self.__previousAction = 'keepGoing'

    def proposeSkipQuestion(self):
        """
        Propose to the players to skip a question
        """
        self.sendTTS('I see that you do not agree at all on a certain answer. Would you like to skip the question ?')
        self.__previousAction = 'proposeSkipQ'

    def paraphraseMessage(self, meaning):
        pass

    # Getters
    def getPreviousAction(self):
        return self.__previousAction

    def getQManager(self):
        return self.__QManager