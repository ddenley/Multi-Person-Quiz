import DecisionMaker
import connection_manager as cm
from typing import Tuple


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
        self.nbTexts = 0                                         # number of texts in the current turn
                                                                 # (typically 1 if just 1 of the players talks)

    def requestNextTurn(self) -> Tuple[str, int, int]:
        """
        Request the next turn of the dialogue to the STT
        :return:
        """
        text, speaker, code = cm.stt_get()
        # TODO - Add code error checks
        return text, speaker, code

    def sendAndRequestNLU(self, text: str, label: int) -> list:
        """
        Send the text from the SST to the NLU to get the intent and the entity of this text.
        :return:
        """
        # TODO - Make sure we can handle multiple entities in a single intent
        nlu_data = cm.rasa_nlu_post(text, str(label))
        intent_name = nlu_data.json()['intent']['name']
        entity_name = None
        entity_value = None
        if len(nlu_data.json()['entities']) > 0:
            entity_name = nlu_data.json()['entities'][0]['entity']
            entity_value = nlu_data.json()['entities'][0]['value']

        return [intent_name, entity_name, entity_value]

    def main(self):
        """
        Main function to handle the dialogue
        """
        self.__DecisionMaker.getAction().introduceQuizz()
        while True:
            # Get the next Turn (transcription of speech to text with label from ASR)
            text, person, code = self.requestNextTurn()
            # TODO - Do something useful with the codes here - 200 is ok, 404 will be no turn found, ....
            if code != 200:
                break

            self.__currentUtt = self.sendAndRequestNLU(text, person)

            self.__onGoing = self.__DecisionMaker.executeRelevantAction(self.__currentUtt,
                                                                        self.__lastUtt, 1, person)

            self.__lastUtt = self.__currentUtt

            # For debug:
            print(text, self.__currentUtt)


if __name__ == '__main__':
    DM = MainDM()
    DM.main()

