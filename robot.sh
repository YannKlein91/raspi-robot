#!/bin/bash
echo "activation env"
which python
cd home/yann/raspi-robot/env
pwd
activate() {
.  home/yann/raspi-robot/env/bin/activate
}
activate
which python
# Is the Xbox Controller connected?
isControllerConnected=$(ls /dev/input | grep event5)

# Is programme ready?
isProgrammeReady=$(ls /home/yann/raspi-robot | grep robot)

# Check if the Xbox Controller is connected.
if [ -n "$isControllerConnected" ]; then
  echo "Command produced isControllerConnected: $isControllerConnected"
  /usr/bin/python3 /home/yann/raspi-robot/robot.py
  while [ -n "$isControllerConnected" ]; do
    isControllerConnected=$(ls /dev/input | grep event5)
    echo "The Xbox Controller is still connected"
    sleep 1
  done
  echo "The Xbox Controller is no longer connected."
else
  echo "The Xbox Controller is not connected."
fi
