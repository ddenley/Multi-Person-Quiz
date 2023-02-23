# Multi-Person-Quiz : Dialogue Manager

First version of the DM. 
Integrated with dummy modules for flask and rasa api integration.

## Important information
The database of the flags need to be in a folder data.
The relative path of the images is 'static/data/flagImg/' and the relative path of the csv file is 'static/data/codes_names.csv'.

This version uses the dummy modules as connections. Test data can be placed 
in the voice-flask.py file. 

This version uses rasa, so it can import an NLU model by placing it in the 
'./models' directory.

## Test this version

To test this version of the DM, use ./script.bash to start the dummy module servers 
and rasa, and then run the MainDM.py file. To stop the severs, enter '3' in the 
script window.

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

