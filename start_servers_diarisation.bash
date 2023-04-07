# Based on https://linuxize.com/post/bash-select/
start_server () {
  python tts/TTS_API.py &
  echo "TTS server started on "$!
  Server1PID=$!

  python GUI_API.py &
  echo "Display server started on "$!
  Server2PID=$!

  python stt/STT_API.py &
  echo "STT server started on "$!
  Server3PID=$!

# Expects a ./models directory, another directory can be specified with -m directory/of/models
  rasa run -i 127.0.0.1 -p 5005 -m models --enable-api &
  echo "RASA server started on "$!
  Server4PID=$!
}

start_dialog_manager() {
  echo "Starting dialog manager"
  python dialogue_manager/MainDM.py -diarisation &
  #python dialogue_manager.py &
  MainPID=$!
}

stop_server () {
 echo "Stopping server PID "$Server1PID
 kill $Server1PID

 echo "Stopping server PID "$Server2PID
 kill $Server2PID

 echo "Stopping server PID "$Server3PID
 kill $Server3PID

 echo "Stopping server PID "$Server4PID
 kill $Server4PID

 echo "Stopping dialog manager PID"$MainPID
 kill $MainPID
}

PS3="Select the operation: "

while true; do
  select opt in start dialog stop quit; do
    case $opt in
      start)
        start_server
        break;;
      dialog)
        start_dialog_manager
        break;;
      stop)
        stop_server
        break;;
      quit)
        exit 0;;
      *)
        echo "Invalid option $REPLY";;
    esac
  done
  echo
done

