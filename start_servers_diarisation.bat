ECHO Running .bat file

start cmd.exe /k python tts/TTS_API.py
start cmd.exe /k python GUI_API.py
start cmd.exe /k rasa run -i 127.0.0.1 -p 5005 -m models --enable-api
echo "Wait for rasa server start then hit any key to start dialogue manager!"
pause
start cmd.exe /k python stt/STT_API.py
start cmd.exe /k python dialogue_manager/MainDM.py -diarisation