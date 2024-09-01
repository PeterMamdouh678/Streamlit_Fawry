FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
openjdk-8-jdk \
wget \
unzip \
lib32stdc++6 \
lib32z1 \
libqt5widgets5 \
libqt5opengl5 \
libqt5gui5 \
libqt5core5a \
libgl1-mesa-glx \
libgl1-mesa-dri \
mesa-utils

# Download and install Android SDK
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip -O tools.zip && \
mkdir -p /sdk && unzip tools.zip -d /sdk && rm tools.zip

# Set environment variables
ENV ANDROID_HOME /sdk
ENV PATH $ANDROID_HOME/cmdline-tools/bin:$PATH

# Install SDK packages and Emulator
RUN yes | sdkmanager --licenses && \
sdkmanager "platform-tools" "platforms;android-30" "emulator" "system-images;android-30;google_apis;x86_64"

# Create an Android AVD
RUN echo "no" | avdmanager create avd -n test_avd -k "system-images;android-30;google_apis;x86_64" -d pixel




import subprocess

def get_emulator_device_name():
# Execute the adb devices command to list all connected devices
result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE)
output = result.stdout.decode("utf-8")

# Extract device names (usually the first column in the output)
device_lines = output.strip().split('\n')[1:] # Skip the first line 'List of devices attached'
devices = [line.split()[0] for line in device_lines if "emulator" in line]

# Return the list of emulator device names
return devices

if __name__ == "__main__":
emulator_devices = get_emulator_device_name()
if emulator_devices:
print("Emulator devices found:")
for device in emulator_devices:
print(device)
else:
print("No emulator devices found.")

