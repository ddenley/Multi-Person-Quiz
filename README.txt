To start the speech to text server run STT_API.py

To test requests run TestingAPI while app is running

Issues:
- Google API error: Exceeded maximum allowed stream duration of 305 seconds
    - Investigating potential solutions - may need to restart server at points
    - First check for reproducibility

Future Work:
- Google API can improve prediction by giving list of expected words

Please be carefull when utilising - limited in amount of minutes we can send audio to the Google API

The audio device set within the STT module will change depending on computer - I will add a script again to help identify the correct audio recording device index for your device.
