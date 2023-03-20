import QuestionManager
import connection_manager as cm
import dialogue_options as do
import requests
import random


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
        :return: msg
        """

        code = cm.tts_post(msg)

        if code != 200:
            print("Error sending path to TTS module.")
            exit(1)
        # Print for debug
        print('- ', msg)
        return msg

    def sendGUI(self, img_path, choices: list):
        """
        Send the path of the image and the multiple choices to the GUI.
        :param img_path:
        :param choices:
        :return:
        """
        code = cm.gui_post(img_path, choices)
        if code != 200:
            print("Error sending path to GUI module.")
            exit(1)

    def introduceQuizz(self):
        """
        Introduce the quizz to the players.
        :return:
        """
        msg = self.sendTTS(do.greeting_options())
        self.__previousAction = 'introQuizz'
        return msg

    def askQuestion(self):
        """
        Ask a question to the players.
        :return:
        """
        self.__previousAction = 'askQuestion'
        self.__QManager.nextQuestion()

        # Send flag image to the GUI server
        self.sendGUI(self.__QManager.getFlagPath(), self.__QManager.getMultipleChoices())
        msg = self.sendTTS(do.question_options(self.__QManager.getMultipleChoices()))

        return msg



    def repeatQuestion(self):
        """
        Repeat the current question - it will ask using different phrasing.
        :return:
        """
        msg1 = self.sendTTS('Absolutely, I can repeat the different choices.')
        msg2 = self.sendTTS(do.question_options(self.__QManager.getMultipleChoices()))
        return msg1+''+msg2
    def checkAgreement(self):
        # NB : This methode seems to be replaced by the methode executeRelevantAction of MainDM class
        pass

    def checkAnswer(self, ans):
        """
        Check the answer of the players and propose a new game.
        :param ans: answer of the players.
        :return:
        """
        self.__previousAction = 'checkAns'
        if ans.casefold() == self.__QManager.getCurrentFlag().casefold():
            self.__QManager.nbSuccess += 1
            msg = self.sendTTS("You agreed on {}. Well done, it's right ! Would you like to continue to play ?".format(ans))
            return msg
        else:
            msg = self.sendTTS("Unfortunately it's not the right answer. This is the flag of {} ! Would you like to try "
                         "another flag ?".format(self.__QManager.getCurrentFlag()))
            return msg
    def ask_finalAnswer(self, ans):
        msg = self.sendTTS("So, is {} your final answer ?".format(ans))
        self.__previousAction = 'ask_finalAnswer'
        return msg

    def engagePlayers(self):
        # TODO : How to engage the discussion between the payers, To be continued
        pass

    def endQuiz(self, pDisagree=False):
        """
        End of the quiz (i.e. the players asked to quit or say no when the bot asked if they want to continue)
        :param pDisagree : boolean which indicates if just one of the player doesn't want to continue/to play
        """
        if pDisagree:
            msg = self.sendTTS("It seems that one of the player doesn't want to play. You need to be two in order to "
                         "discuss together. Please come again when all of the players want to play")
        else:
            msg = self.sendTTS('I understand, see you later !')
        # Should the bot display the results of the quiz ?! (i.e. number/percentage of successes)
        return msg

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
        msg = self.sendTTS('I see that you do not agree at all on a certain answer. Would you like to skip the question ?')
        self.__previousAction = 'proposeSkipQ'
        return msg

    def proposeClue(self):
        """
        Propose to the players to ask for a clue
        """
        msg = self.sendTTS('This is a tough one, would you like a clue? ?')
        self.__previousAction = 'proposeClue'
        return msg

    def giveClue(self):
        """
        Give a clue to the players about the current question
        :return:
        """
        clue = do.provide_clue(self.__QManager.getCurrentFlag())
        msg = 'Think about this hint. We are talking about {}'.format(clue)
        self.sendTTS(msg)
        self.__previousAction = 'giveClue'
        return msg

    def confirm(self, skip=False, ans=None):
        """
        Confirm to the players about what they asked the bot
        :param skip: boolean, True if the players asked the bot to skip the question
        :return:
        """
        msg = ''
        if skip:
            msg = self.sendTTS("Ok, let's skip this question !")
        elif ans is not None:
            msg = self.ask_finalAnswer(ans)
            self.__previousAction = 'confirm_ans'
        return msg

    def paraphraseMessage(self, meaning):
        pass

    # Getters
    def getPreviousAction(self):
        return self.__previousAction

    def getQManager(self):
        return self.__QManager
