# Multi-Person-Quiz
Team repo for conversational agents and spoken language processing. Developing a multi-person quiz game.

## Branch : Alex Week 3

Attempted to automatize a system of question-answer based on what has been seen in previous labs and the work of Andy.
Didn't quite succeed using the formalism used by Andy, especially the "forms" feature, so I kept using only the entity "answer". The chatbot is rather simple and uses a loop (thanks to checkpoint) to ask questions and check the answer of the user. Key part of the work is the custom actions ask_question and check_answer which keep track of the user's state (question and score). I am confident that we could generalize and complexify what I've done though, by using multiple entities (if necessary) and forms in the future.

Here is a story diagram of the chatbot for the moment

![ca_wk3](https://user-images.githubusercontent.com/92320638/216168429-51fca261-da3f-4b08-92ea-92435a2cce48.png)


## Launching

In a 1st terminal, run the command line : <rasa run actions> which will allow the chatbot to read in the actions file.
It seems that every time you edit the actions file, you will not only need to save the project, but also kill the port 5055 (by for example the command line <npx kill-port 5055>) and restart it by <rasa run actions> but I might be mistaken.

In a 2nd terminal, <rasa train> then <rasa shell>.
