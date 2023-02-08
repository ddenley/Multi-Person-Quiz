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
- investigate on the possibility of another model, or specifying it more, since for the moment intent classification may occur.
Futhermore, current model would have a lot of difficulties dealling with complex, especially hesitant, answers, such as "i think it is (answer1) ... Wait, actually i think it is rather (answer2)" or "you're wrong ... Oh, sorry, i actually think you're right".
__PERSONAL THOUGHT__ : Maybe we could have fewer intents like only give_answer, instead of concur/contest, and we could track the answers more specifically like :
(intent give answer) I don't think it is [Norway](entity: answer, role: deny), but rather [Sweden](entity: answer, role: final_answer). It could be easier then to track the final answer of an user and ignore the others.

## Launching

In a 1st terminal, run the command line : __rasa run actions__ which will allow the chatbot to read in the actions file.
It seems that every time you edit the actions file, you will not only need to save the project, but also kill the port 5055 (by for example the command line __npx kill-port 5055__) and restart it by __rasa run actions__ but I might be mistaken.

In a 2nd terminal, __rasa train__ then __rasa shell__ (or __rasa interactive__ to have interactive options).
