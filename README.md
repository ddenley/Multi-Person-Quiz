# Detecting agreement in multi-party dialogue: evaluating speaker diarisation versus a procedural baseline to enhance user engagement.

This is the code related with our study on : multi-person collaborative flag quiz for social robots in public spaces.

*Conversational agents participating in multi-party interactions face significant challenges in dialogue state tracking, since the identity of the speaker adds significant contextual meaning. It is common to utilise diarisation models to identify the speaker. However, it is not clear if these are accurate enough to correctly identify specific conversational events such as agreement or disagreement during a real-time interaction. This study uses a cooperative quiz, where the conversational agent acts as quiz-show host, to determine whether diarisation or a frequency-and-proximity-based method is more accurate at determining agreement, and whether this translates to feelings of engagement from the players.Experimental results show that our proposed method was preferred by players, and was more accurate at detecting agreement, reaching an accuracy of 0.44, compared to 0.28 for the diarised system.*



## Installation

Install all the libraries:

```bash
pip install -r requirement.txt
```
Add your API credentials in the file google_api_credentials.json for STT and TTS of google
[Google STT](https://cloud.google.com/speech-to-text)
[Google TTS](https://cloud.google.com/text-to-speech)

## Usage

### Diarised version

**On windows:**

```powershell
.\start_servers_diarisation.bat
```

**On linux:**

```bash
./start_servers_diarisation.bash
```

### Non-Diarised version

**On windows:**

```powershell
.\start_servers.bat
```

**On linux:**

```bash
./start_servers.bash
```
## Test testing 
The branch "nlu_test" is dedicated to test new version of nlu 

## Authors
- [Alexandre Kha](https://github.com/Ottogod): apk2002@hw.ac.uk
- [Andy Edmondson](https://github.com/Levinin): ae2016@hw.ac.uk
- [Daniel Denley](https://github.com/ddenley): dad2001@hw.ac.uk
- James Ndubuisi: jn2033@hw.ac.uk
- [Lia Perochaud](https://github.com/Lisnivia): lfrp2000@hw.ac.uk
- Miebaka Worika: mw2037@hw.ac.uk
- Neil O’Reilly: no2003@hw.ac.uk
- [Raphaël Valeri](https://github.com/RaphValeri): rv2018@hw.ac.uk

School of Mathematical and Computer Sciences, Heriot-Watt University, Edinburgh

## License

[MIT](https://choosealicense.com/licenses/mit/)


