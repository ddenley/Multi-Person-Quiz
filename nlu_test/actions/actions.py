# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import List, Dict, Any, Union, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import random


#from rasa_sdk import FormAction

questions = {
	"What is the country of Edinburgh ?" : "Scotland",
	"What is the country of Paris ?" : "France",
	"What is the country of Brussels ?": "Belgium",
	"What is the country of Rangoon ?": "Myanmar",
	"What is the country of New York ?": "United States"
}



current_answer = "std"
current_answer2 = "bonjours"

current_answers = ["std", "bonjours"]
turn = 0

accepted_answers_1 = []
accepted_answers_2 = []
accepted_answers = {0:[], 1:[]}

nb_question = len(list(questions.keys()))



class ActionAskQuestion(Action):
	

	def name(self) -> Text:
			return "action_ask_question"

	def run(self,
	dispatcher: CollectingDispatcher, 
	tracker: Tracker, 
	domain:  Dict[Text, Any]) -> List[Dict[Text, Any]]:
		global questions
		
		l = list(questions.items())
		random.shuffle(l)
		questions = dict(l)
		
		response = list(questions.keys())[0]

		dispatcher.utter_message(text = response)
		return []

"""
class ActionUpdateAnswer(Action):

	

	def name(self) -> Text:
			return "action_update_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global  current_answers, turn

		current_answers[0] = tracker.get_slot("answer1")
		dispatcher.utter_message(text = "Turn {}. Player 1 says : {}. What do you think Player 2 ?".format(turn, current_answers[0]))

		return [SlotSet("answer1",None)]


	

class ActionCheckAnswer(Action):


	def name(self) -> Text:
			return "action_check_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global turn, questions
			
		correct_answer = list(questions.values())[0]

		turn += 1
		mod_turn = turn%2 

		current_answers[mod_turn] = tracker.get_slot("answer1")
		if current_answers[mod_turn] == None:
				current_answers[mod_turn] = current_answers[(mod_turn + 1)%2]

		if current_answers[0].lower() == current_answers[1].lower():
			if current_answers[0].lower() == correct_answer.lower():
				response = "Turn {}. Correct! The answer is indeed {}.".format(turn, correct_answer)
			else:
				response = "Turn {}. Incorrect, it is not {}. The answer is : {}.".format(turn, current_answers[0], correct_answer)
			turn = 0
			
		else :
			response = "Turn {}. Player 1 says {}, Player 2 says {}. You don't seem to agree. What do you think Player {} ?".format(turn, current_answers[0].lower(), current_answers[1].lower(), (mod_turn + 1)%2 + 1)
		

		dispatcher.utter_message(text = response)

		return [SlotSet("answer1", None)]
"""
		
class ActionUpdateAnswer(Action):

	def name(self) -> Text:
			return "action_update_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global  accepted_answers, turn

		for entity in tracker.latest_message["entities"]:
			if entity["entity"] == "answer" and entity["value"].lower() not in accepted_answers[0]:
				accepted_answers[0].append(entity["value"].lower())
		dispatcher.utter_message(text = "Turn {}. Player 1 says : {}. What do you think Player 2 ?".format(turn, accepted_answers[0]))

		return []


class ActionCheckAnswer(Action):


	def name(self) -> Text:
			return "action_check_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global accepted_answers, turn, questions
			
		correct_answer = list(questions.values())[0]

		turn += 1
		mod_turn = turn%2 

		answers = []
		for entity in tracker.latest_message["entities"]:
			if entity["entity"] == "answer" and entity["value"].lower() not in accepted_answers[mod_turn]:
				accepted_answers[mod_turn].append(entity["value"].lower())

		if not accepted_answers[mod_turn]:
			accepted_answers[mod_turn] = accepted_answers[(mod_turn + 1)%2]

		answer1 = accepted_answers[0][-1]
		answer2 = accepted_answers[1][-1]

		if answer1.lower() == answer2.lower():
			if answer1.lower() == correct_answer.lower():
				response = "Turn {}. Correct! The answer is indeed {}.".format(turn, correct_answer)
			else:
				response = "Turn {}. Incorrect, it is not {}. The answer is : {}.".format(turn, answer2, correct_answer)
			accepted_answers = {0:[], 1:[]}
			turn = 0

			dispatcher.utter_message(text = response)
			return []

		"""
		for answer in accepted_answers[0]:
			if answer in accepted_answers[1]:
				if answer.lower() == correct_answer.lower():
					response = "Turn {}. Correct! The answer is indeed {}.".format(turn, correct_answer)
				else:
					response = "Turn {}. Incorrect, it is not {}. The answer is : {}.".format(turn, answer, correct_answer)
				accepted_answers = {0:[], 1:[]}
				turn = 0

				dispatcher.utter_message(text = response)
				return []
		"""

		response = "Turn {}. Player 1 says {}, Player 2 says {}. You don't seem to agree. What do you think Player {} ?".format(turn, accepted_answers[0], accepted_answers[1], (mod_turn + 1)%2 + 1)
		dispatcher.utter_message(text = response)

		return []
