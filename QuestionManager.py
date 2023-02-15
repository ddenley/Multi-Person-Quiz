import pandas as pd
import matplotlib.pyplot as plt
import cv2
import random
import os


class QuestionManager:
    """
    Handle the management of the flag questions during the Multi-person Quizz
    """

    def __init__(self):
        """
        Constructor of the class QuestionManager which initializes the main attributes and load the data
        """
        # Attributes related to the database of the flags
        self.img_list = None
        self.img_path = None
        self.__currentImgPath = None

        self.country_codes = None
        self.name_df = None
        self.name_lookup = None

        # Attributes to store previous and current information about the question
        self.__previousFlag = None
        self.__currentChoices = ['', '', '', '']
        self.__currentFlag = None
        self.nbSuccess = 0
        self.__idxQ = 0

        # Load the data and initialize the attributes
        self.loadData()
        self.reinitialize()


    def reinitialize(self):
        """
        Reinitialize the Object by setting all the attributes to their default values
        :return:
        """
        self.__idxQ = 0  # number of questions asked to the players
        self.__nbSuccess = 0  # number of success during the game
        # Attributes about the current question
        self.__currentImgPath = None
        self.__currentFlag = None
        self.__currentChoices = ['', '', '', '']
        # Store the previous questions
        self.__previousFlag = []  # list with the names of each flag already asked

    def nextQuestion(self):
        """
        Get a new random question from the database
        :return:
        """
        # Get a random new flag
        n = ''
        for _ in range(200):
            n = random.choice(self.img_list)
            if (n[0:2].upper() in self.name_lookup) and not (n in self.__previousFlag):
                break
        # Get the country name corresponding to the flag
        self.__currentImgPath = n
        country_code = n[0:2].upper()
        self.__currentFlag = self.name_lookup[country_code]
        # Add this name in the list of the choices
        self.__currentChoices[0] = self.__currentFlag
        # Add three other different country names
        self.getMulitpleChoices()
        # Shuffle the list of the choices
        random.shuffle(self.__currentChoices)

    def displayFlag(self):
        """
        Display a flag for test visualization
        :return:
        """
        img = cv2.imread(os.path.join(self.img_path, self.__currentImgPath))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.figure()
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title('Which flag is it ?')
        plt.show()

    def getMulitpleChoices(self):
        """
        Get three random possible answers to give a list of multiple choices to the user
        :return:
        """
        for i in range(1, 4):
            # Get three different random country names
            country = self.__currentFlag
            while country in self.__currentChoices:
                code = random.choice(list(self.name_lookup.keys()))
                country = self.name_lookup[code]
            self.__currentChoices[i] = country

    def loadData(self):
        """
        Load the data

        This function uses code from the proof of concept by Andy Edmondson
        :return:
        """

        self.img_path = os.path.join('data/imgFlags/')
        self.img_list = os.listdir(self.img_path)

        # Filenames contain country abbreviations, so create a list of these
        self.country_codes = [fname[0:2] for fname in self.img_list]

        # Create a lookup dict for the country codes
        self.name_df = pd.read_csv("data/codes_names.csv")  # , encoding="iso-8859-1")
        self.name_lookup = dict([(code, name) for code, name in
                                 zip(self.name_df["code2"], self.name_df["name"])])

    # Getters

    def getCurrentFlag(self):
        return self.__currentFlag

    def getMultipleChoices(self):
        return self.__currentChoices


if __name__=='__main__':
    # Test the main functions of the class
    QManager = QuestionManager()
    QManager.nextQuestion()
    choices = QManager.getMultipleChoices()
    for i in range(len(choices)):
        print('{} : {}'.format(i, choices[i]))
    QManager.displayFlag()
