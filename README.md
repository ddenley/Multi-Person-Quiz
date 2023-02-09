# Multi-Person-Quiz : Dialogue Manager

First version of the DM. 

## Important information
The database of the flags need to be in a folder data.
The relative path of the images is 'data/imgFlags/' and the relative path of the csv file is 'data/codes_names.csv'.

For the moment, there are no links between the DM and the STT, the DM and the NLU and the DM and the NLG/GUI. That is 
why the functions *requestNextTurn()* and *sendAndRequestNLU()* are more close of a simulation of what can return the STT
and the NLU than a right implementation to request the information.

Moreover, the main function which makes the decision-making process is *executeRelevantAction()* in the class MainDM. 
This function doesn't cover all the possible cases (just few cases for the moment).

TODO : Implement a class DecisionMaker 

## Test this version

To test this version of the DM you can execute the  MainDM.py file.
This should simulate a dialogue like this one:


- Hey! Would you like to play a game ? You must associate each flag with its country.

- Yes, for sure

- What is this flag ?

    0 : South Africa

    1 : Iceland

    2 : United Kingdom

    3 : Trinidad and Tobago

- Mhmm, I think it is United Kingdom, what do you think ?
- Yes, probably
- Well done, it's right ! Would you like to continue to play ?

