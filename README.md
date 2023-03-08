# Multi-Person-Quiz : NLU

## Progress on week 4

- Prototype bot for testing NLU. Questions are in the form "what is the country of Edinburgh ?" since there is no option for displaying flags yet. __NOTA BENE__ : Stories and actions are purely experimental and do not align with the real Dialogue Management part of the project (Raphaël).
- Added lookup table for the entity answer, which gathers all the different countries (see nlu file). Have to add synonyms in the future (e.g. US = USA = United States etc.)
- 3 main intents for the moment : give_answer, concur/agree, contest/disagree (nlu file). __WARNING__ : entities are often recognized but intents can be misclassified (overlapping intents). E.g. "Yeah I think it is [Norway](answer)" could be misclassified as "give_answer" whereas it is "concur"
- __NOTA BENE__: May uncomment the config file part about the pipeline from RegexExtrctor to FallbackClassifier (didn't notice results improvemet though)

Here is the ideal (without the interactive stories) story diagram of the current chatbot:

<p align="center">
  <img src="https://user-images.githubusercontent.com/92320638/217417787-3b14aa15-e75a-4ac5-adc8-bc9dc9a3bb09.png" 
       width="500" 
       height="600"/>
</p>


### Points to improve

- maybe add other intents to make the model more complete (eg repeatQuestion, skipQuestion, etc (see evaluation file))
- better slot management (eg an answer slot for user 1 and another one for user 2) 
- use forms as active loops to listen to the users until all required slots (eventually yet to be defined) are filled 
- investigate on the possibility of another model, or specifying it more, since for the moment intent misclassification may occur.
Futhermore, current model would have a lot of difficulties dealling with complex, especially hesitant, answers, such as "i think it is (answer1) ... Wait, actually i think it is rather (answer2)" or "you're wrong ... Oh, sorry, i actually think you're right".

__PERSONAL THOUGHT__ : Maybe we could have fewer intents like only give_answer, instead of concur/contest, and we could track the answers more specifically like :
(intent give answer) I don't think it is [Norway](entity: answer, role: deny), but rather [Sweden](entity: answer, role: final_answer). It could be easier then to track the final answer of a user, and ignore the others.



## Progress on week 5

- Simplified version of chatbot, with no checkpoint anymore. They were indeed hard to read and induced too much training time. Furthermore we do not work on the DM part so we just need some simple stories which can be verified easily
- One quiz question taken randomly and asked to the users
- Turn by turn system which signals who has spoken and who must speak. Stories don't go further than ~3 turns though
- We use a 2-element list __current_answers__ in the custom actions file. The first element stores the answer of user 1, while the second one stores the answer of user 2. __check_answer__ then assesses whether or not these elements match, if so, it displays the correct answer; if not, the bot continues to listen
- A lot more examples for each of the 3 previous intents, labelled automatically and in such a way that we reduce intent overlapping (same countries for all intents)


Current story diagram (rasa visualize) :

<p align="center">
  <img src="https://user-images.githubusercontent.com/92320638/220176031-b84ebe69-282a-46cb-be16-8a6082790c3b.png" 
       width="500" 
       height="600"/>
</p>


### Points to improve / do

- Integrate Data collection work
- introduce other variations to express more accurately intents
- Deal with synonyms (USA = US = United States ..., Vatican city = Vatican, Myanmar = Burma etc.)
- Answers can also be letters (__A__, __B__, __C__, __D__)
- implement test stories, which would help for model evaluation

### Nota Bene
The action __action_update_answer__ is in fact the registering of the first answer (therefore, made by "user 1"). It doesn't check anything (since "user 2" hasn't spoken yet). Afterward, it is never used again, we use rather __action_check_answer__ to do the next updates and answer checks (to see if the answers of each match). May have to rename it in __initial_answer_update__ for example.

## Progress on week 6

### 23/02
- Detecting Option A, ..., Option D as answers
- removing a confusing example "no way it is ..." because it didn't recognize well any intent with the entity "Norway"

### Plan for the week end
- No need to specify slots examples or their quantity in story, use rather tracker.get_latest_message to store in a slot list
- When someone suggests multiple choices like "Maybe it is (denmark) or (sweden)", we store both in a suggestion list for each player
- use roles : Accepted & Denied. indeed we have to differenciate answers in cases like "I think it is (France)(answer:accepted)" and "I don't think it is (france)(answer:denied)"
- Discussion intent. __WARNING__ : Likely to overlap other intents 

## Progress on week 7 & 8

- Data Collection integrated
- Data augmentation on composed country names
- Data augmentation using standardized examples
- Tests & evaluation (cf Results) using different pipeline configurations. Standard one (DIET classifier + Regex Extractor) has most notable trade-off in computation time / metrics. Integrated language model BERT gives very good metrics (>98%)  

## Launching

In a 1st terminal, run the command line : __rasa run actions__ which will allow the chatbot to read in the actions file.
It seems that every time you edit the actions file, you will not only need to save the project, but also kill the port 5055 (by for example the command line __npx kill-port 5055__) and restart it by __rasa run actions__ but I might be mistaken.

In a 2nd terminal, __rasa train__ then __rasa shell__ (or __rasa interactive__ to have interactive options).
