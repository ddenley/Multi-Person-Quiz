import pandas as pd
import matplotlib.pyplot as plt
import cv2
import random
import os
import numpy as np


class QuestionManager:
    """
    Handle the management of the flag questions during the Multi-person Quizz
    """

    def __init__(self):
        """
        Constructor of the class QuestionManager which initializes the main attributes and load the data
        """
        # Attributes related to the database of the flags
        self.img_path = 'static/data/img/'
        self.img_list = None
        self.__currentImgPath = None
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
        self.nextQuestion()         # Make sure the values are not left empty in case of a query.

    def nextQuestion(self):
        """
        Get a new random question from the database
        :return:
        """
        # TODO : Do we need to ensure to display a different question than the one already asked ? (i.e. check that
        #  that the new Flag has not already been asked ?)
        self.__currentChoices = np.random.choice(list(self.name_lookup.keys()), 4, replace=False).tolist()
        self.__currentFlag = self.__currentChoices[0]  # Always choose the first option as the answer

        # Shuffle so they are in a random order to the player
        random.shuffle(self.__currentChoices)

        # The filename is lowercase country code.png
        answer_code = self.name_lookup[self.__currentFlag]
        self.__currentImgPath = os.path.join(self.img_path, answer_code.lower() + ".png")

    def displayFlag(self):
        """
        Display a flag for test visualization
        :return:
        """
        img = cv2.imread(self.__currentImgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.figure()
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title('Which flag is it ?')
        plt.show()

    def loadData(self):
        """
        Load the data

        This function uses code from the proof of concept by Andy Edmondson
        :return:
        """
        self.img_list = os.listdir(self.img_path)

        # Create a lookup dict for the country codes
        name_df = pd.read_csv("static/data/codes_names.csv")
        self.name_lookup = dict([(name, code) for code, name in
                                 zip(name_df["code2"], name_df["name"])])

    # Getters

    def getCurrentFlag(self) -> str:
        return self.__currentFlag

    def getMultipleChoices(self) -> list:
        return self.__currentChoices

    def getFlagPath(self) -> str:
        return self.__currentImgPath


if __name__=='__main__':
    # Test the main functions of the class
    QManager = QuestionManager()
    QManager.nextQuestion()
    choices = QManager.getMultipleChoices()
    for i in range(len(choices)):
        print('{} : {}'.format(i, choices[i]))
    QManager.displayFlag()
    print(QManager.getCurrentFlag())
