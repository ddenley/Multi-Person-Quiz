import DecisionMaker
import connection_manager as cm
from typing import Tuple
import datetime
import DecisionMaker_with_diarisation
import sys



class MainDM:
    """
    Main class of the Dialogue Management of the project Multi-Person Quizz.
    This class handle the flow of the information between the STT and the NLU to get the label, intent and the entity for each utterance,
    and trigger the action which seems the most relevant using the DecisionMaker class.
    """

    def __init__(self):
        self.__onGoing = True  # boolean to indicate if a game is in progress

        self.multipleChoices = True #booloean to indicates if the game uses multiple choices or not
        self.verbose = True
        if len(sys.argv) == 1:
            print("Run non-diarised version")
            self.diarisation = False
        else:
            print("Run diarised version")
            self.diarisation = True

        # Index to do a test version
        self.idxNTurn = 0
        self.idxNLU = 0

        if (self.diarisation == True):
            self.__DecisionMaker = DecisionMaker_with_diarisation.DecisionMaker(self.multipleChoices, self.verbose)  # DecisionMaker with diarisation instance
        else:
            self.__DecisionMaker = DecisionMaker.DecisionMaker(self.multipleChoices, self.verbose)  # DecisionMaker without diarisationinstance

        self.__previousTurns = {'0': [], '1': []}  # dictionary for previous turns for each person
        self.currentLabel = '0'
        self.__currentUtt = ['', '', '']  # list for current turn [intent, entity, label]
        self.__lastUtt = ['', '', '']  # list of the previous turn [intent, entity, label]
        self.__currentAnswer = ''  # current Answer of the participants
        self.nbTexts = 0  # number of texts in the current turn
        # (typically 1 if just 1 of the players talks)

    def initialize(self):
        """
        Initialize the instances variables before playing a game (avoid the need to kill each PID and restart the
        server for each game)

        :return:
        """
        self.__onGoing = True  # boolean to indicate if a game is in progress

        # Index to do a test version
        self.idxNTurn = 0
        self.idxNLU = 0

        self.__DecisionMaker = DecisionMaker.DecisionMaker(self.multipleChoices, self.verbose)  # DecisionMaker instance

        self.__previousTurns = {'0': [], '1': []}  # dictionary for previous turns for each person
        self.currentLabel = '0'
        self.__currentUtt = ['', '', '']  # list for current turn [intent, entity, label]
        self.__lastUtt = ['', '', '']  # list of the previous turn [intent, entity, label]
        self.__currentAnswer = ''  # current Answer of the participants
        self.nbTexts = 0  # number of texts in the current turn
        # (typically 1 if just 1 of the players talks)

    def requestNextTurn(self) -> list:
        """
        Request the next turn of the dialogue to the STT
        :return: list containing the turn text, speaker and API return code.
        """
        text, speaker, code = cm.stt_get()
        # TODO - Add code error checks
        return [text, speaker, code]

    def get_turn_batch(self, max_batch_size: int = 1) -> list:
        """Get a batch of turns for processing.
        :return: list of turn data lists."""
        batch = []
        for _ in range(max_batch_size):
            turn = self.requestNextTurn()
            batch.append(turn)
            if turn[2] != 200:
                break
        return batch

    # def sendAndRequestNLU(self, text: str, label: int) -> list:
    #     """
    #     Send the text from the SST to the NLU to get the intent and the entity of this text.
    #     :return:
    #     """
    #     # TODO - Make sure we can handle multiple entities in a single turn
    #     nlu_data = cm.rasa_nlu_post(text, str(label))
    #     intent_name = nlu_data.json()['intent']['name']
    #     entity_name = None
    #     entity_value = None
    #     if len(nlu_data.json()['entities']) > 0:
    #         entity_name = nlu_data.json()['entities'][0]['entity']
    #         entity_value = nlu_data.json()['entities'][0]['value']
    #
    #     return [intent_name, [entity_name], [entity_value]]

    def sendAndRequestNLU(self, text: str, label: int) -> list:
        """
        Send the text from the SST to the NLU to get the intent and the entity of this text.
        :return:
        """
        # TODO - Make sure we can handle multiple entities in a single turn
        nlu_data = cm.rasa_nlu_post(text, str(label))
        intent_name = nlu_data.json()['intent']['name']
        entity_name = None
        entity_value = None
        if len(nlu_data.json()['entities']) > 0:
            # Find the first valid entity in the list
            for e in nlu_data.json()['entities']:
                if e['value'] in ["the", "a", "is"]:
                    continue
                entity_name = e['entity']
                entity_value = e['value']
                break

        return [intent_name, [entity_name], [entity_value]]

    def init_backup(self, msg):
        """
        Create a text file to save the dialog.
        """
        # Get the time to use it in the name of the text file
        t0 = datetime.datetime.now()
        filename = 'MultiQuiz_dialog_{}{}{}-{}_{}.txt'.format(t0.year, t0.month, t0.day, t0.hour, t0.minute)
        # print(filename)
        # Create the text file and write the first message
        f = open(filename, "w+")
        f.write(msg)
        f.close()
        return filename

    def save_backup(self, filename, storedDialog):
        f = open(filename, "a")
        for i in range(len(storedDialog)):
            f.write(storedDialog[i])
        f.close()

    def main(self):
        """
        Main function to handle the dialogue
        """

        self.initialize()
        msg = self.__DecisionMaker.getAction().introduceQuizz() + '\n'
        filename = self.init_backup(msg)
        while self.__onGoing:
            # Get the next Turn batch (transcription of speech to text with label from ASR)
            turn_batch = self.get_turn_batch(1)

            for turn in turn_batch:
                storedDialog = []
                # Unpack the turn for clarity
                text, person, code = turn

                # TODO - Do something useful with the codes here - 200 is ok, 404 will be no turn found, ....
                #        Make sure all of the codes Daniel is sending are managed.

                # HTTP_204_NO_CONTENT may be returned by STT_API.py
                if code == 204:
                    continue

                # If some other code not handled here, exit.
                if code != 200:
                    self.__onGoing = False
                    break
                self.__currentUtt = self.sendAndRequestNLU(text, person)
                # For debug (display the text and the NLU analysis before the action is triggered) and stored to a
                # list to write in a text file:
                print(text, self.__currentUtt, person)
                currentTurn = ' P{} : {} {} \n'.format(person, text, self.__currentUtt)
                storedDialog.append(currentTurn)

                self.__onGoing, msgBot = self.__DecisionMaker.executeRelevantAction(self.__currentUtt, person-1) #person-1 just to map the 0 and 1 in the decision-making process now
                botText = 'S : {} \n'.format(msgBot)
                storedDialog.append(botText)

                if not self.__onGoing:
                    break

                self.__lastUtt = self.__currentUtt
                self.save_backup(filename, storedDialog)
                if self.verbose:
                    txt = self.__DecisionMaker.print_vars()
                    self.save_backup(filename, txt)


if __name__ == '__main__':
    DM = MainDM()
    DM.main()
    # dm.sendAndRequestNLU()
