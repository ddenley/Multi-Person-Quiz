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

nb_question = len(list(questions.keys()))
indx = 0
score = 0



class ActionAskQuestion(Action):
	

	def name(self) -> Text:
			return "action_ask_question"

	def run(self,
	dispatcher: CollectingDispatcher, 
	tracker: Tracker, 
	domain:  Dict[Text, Any]) -> List[Dict[Text, Any]]:
		
		global indx, nb_question, questions

		# shuffle randomly the dictionary
		if indx == 0:
			l = list(questions.items())
			random.shuffle(l)
			questions = dict(l)

		
		if indx < nb_question:
			response = list(questions.keys())[indx]
		# should never happen
		else:
			response = "There is no more questions, you completed the quiz !"

		dispatcher.utter_message(text = response)

		#return [SlotSet("answer", None)]
		return []

class ActionUpdateAnswer(Action):
	

	def name(self) -> Text:
			return "action_update_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global indx, nb_question, score, current_answer
			
		
		current_answer = tracker.get_slot("answer")

		return [SlotSet("answer", current_answer)]

class ActionCheckAnswer(Action):
	

	def name(self) -> Text:
			return "action_check_answer"

	def run(self, 
			dispatcher: CollectingDispatcher, 
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		global indx, nb_question, score, current_answer
			
		correct_answer = list(questions.values())[indx]

		if current_answer.lower() == correct_answer.lower():
			response = "Correct! The answer is indeed {}.".format(correct_answer)
			score += 1
		else:
			response = "Incorrect, it is not {}. The answer is : {}.".format(current_answer, correct_answer)
		indx += 1

		if indx == nb_question :
			response = response + " There is no more questions, you completed the quiz ! Your score is {}/{}.".format(score, nb_question)
			indx = 0
			score = 0


		dispatcher.utter_message(text = response)

		#return [SlotSet("answer", None)]
		return [SlotSet("answer", None)]



"""
def get_next_question(questions, current):
	questions_keys = list(questions.keys())
	current_index = questions_keys.index(current_question)

	#check if there are still questions
	if current_index +1< len(question_keys):
		return question_keys[current_index + 1]
	# No question anymore
	else :
		return None
"""

"""
class CheckAnswer(Action):

	def name(self) -> Text:
		return "action_check_answer"

	def run(self, dispatcher, tracker, domain):
		correct_answer = tracker.get_slot("correct_answer")
		user_answer = tracker.get_slot("answer")

		if user_answer == correct_answer:
			response = "Correct! The answer is indeed {}. Would you like to continue ?"
		else:
			response = "Incorrect. The answer is : {} . Would you like to continue ?".format(correct_answer)

		dispatcher.utter_message(text = response)

		return [SlotSet("answer", None), SlotSet("correct_answer", None)]
"""

"""
class ActionSetInitialQuestion(Action):
	def name(self) -> Text:
		return "action_set_initial_question"

	def run(self, dispatcher, tracker, domain):
		correct_answer = list(question.keys())[indx]
		user_answer = tracker.get_slot("answer")

		if user_answer == correct_answer:
			response = "Correct! Would you like to continue the quiz ?"
		else:
			response = "Incorrect. The answer was : {} .Would you like to continue the quiz ?".format(correct_answer)

		dispatcher.utter_message(text = response)

		return [SlotSet("answer", None)]
"""

"""
class QuizForm(FormAction):

	def name(self) -> Text:
		return "quiz_form"

	@staticmethod
	def required_slots(tracker : Tracker) -> List[Text]:
		return ["answer"]

	def slot_mappings(self):
		return {
			"answer": self.from_text(entity="answer")
		}

	def submit(
		self, 
		dispatcher: CollectingDispatcher,
		tracker: Tracker, 
		domain: Dict[Text, Any]
		) -> List[Dict]:

		current_question = tracker.get_slot("current_question")
		answer = tracker.get_slot("answer")
		correct_answer = questions.get(current_question)

		# compare answer and correct answer
		if answer == correct_answer:
			dispatcher.utter_message("Correct ! The answer is indeed {}.".format(correct_answer))

			next_question = get_next_question(questions, current_question)

			if next_question:
				return [SlotSet("current_question", next_question)]
			else:
				return [ SlotSet("current_question", None), SlotSet("answer", None)]

		else:
			dispatcher.utter_message("Incorrect. the answer is {}".format(correct_answer)
			return [SlotSet("answer", None)]
"""