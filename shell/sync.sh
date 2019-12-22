#!/bin/sh

if curl owly.dedyn.io
then
  find "$HOME/Pictures/" | md5sum > /tmp/before_sync.txt
  rclone sync PhotoFrame:fotos_mama "$HOME/Pictures/"
  find "$HOME/Pictures/" | md5sum > /tmp/after_sync.txt

  if [ "$(cat /tmp/before_sync.txt)" != "$(cat /tmp/after_sync.txt)" ]
  then
    skill -USR1 "$(pgrep -f python photo_frame.py)"
  fi
fi
