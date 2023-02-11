# Based on https://linuxize.com/post/bash-select/

start_server () {
  python tts-flask.py &
  echo "TTS server started on "$!
  Server1PID=$!

  python display-flask.py &
  echo "Display server started on "$!
  Server2PID=$!

  python voice-flask.py &
  echo "STT server started on "$!
  Server3PID=$!

# Expects a ./models directory, another directory can be specified with -m directory/of/models
  rasa run -i 127.0.0.1 -p 5005 -m models --enable-api &
  echo "RASA server started on "$!
  Server4PID=$!
}

start_dialog_manager() {
  echo "Starting dialog manager"
  python dialogue_manager.py &
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
}


PS3="Select the operation: "

select opt in start dialog stop quit; do

  case $opt in
    start)
      start_server;;
    dialog)
      start_dialog_manager;;
    stop)
      stop_server;;
    quit)
      break;;
    *) 
      echo "Invalid option $REPLY";;
  esac
done
