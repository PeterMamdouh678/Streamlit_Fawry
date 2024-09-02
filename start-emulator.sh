#!/bin/bash

# Start the emulator in the background with logging
echo "Starting Android Emulator..."
/sdk/emulator/emulator -avd test -no-window -no-audio -no-boot-anim -verbose > /emulator.log 2>&1 &

# Set a timeout for the boot process
BOOT_TIMEOUT=350 # 5 minutes
SECONDS=0

# Wait for the emulator to boot up
echo "Waiting for emulator to be ready..."
adb wait-for-device
until adb shell getprop sys.boot_completed | grep -q 1; do
  if [ $SECONDS -gt $BOOT_TIMEOUT ]; then
    echo "Emulator failed to boot within the timeout period"
    exit 1
  fi
  echo "Still waiting for emulator to finish booting..."
  sleep 5
done

# Confirm the emulator is up and running
echo "Emulator is up and running."
