# FROM ubuntu:20.04
FROM python:3.10
WORKDIR /deploy

# Install system dependencies
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g appium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update repositories and install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
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
    mesa-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

COPY . /Deploy      
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt
# Download and install Android SDK
# RUN wget https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip -O tools.zip && \
# mkdir -p /sdk && unzip tools.zip -d /sdk && rm tools.zip


# RUN mkdir /android-sdk && cd /android-sdk && \
#     wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip -O tools.zip && \
#     unzip tools.zip && \
#     rm tools.zip && \
#     mkdir ~/.android && touch ~/.android/repositories.cfg && \
#     yes | /android-sdk/cmdline-tools/bin/sdkmanager --licenses && \
#     /android-sdk/cmdline-tools/bin/sdkmanager "platform-tools" "platforms;android-30" "build-tools;30.0.3" "emulator" "system-images;android-30;google_apis;x86_64" "extras;intel;Hardware_Accelerated_Execution_Manager"

# Install Android SDK
RUN mkdir -p /sdk/cmdline-tools/latest && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip -O cmdline-tools.zip && \
    unzip cmdline-tools.zip -d /sdk/cmdline-tools && \
    rm cmdline-tools.zip && \
    mv /sdk/cmdline-tools/cmdline-tools/* /sdk/cmdline-tools/latest/ && \
    rmdir /sdk/cmdline-tools/cmdline-tools

# Accept licenses and install necessary SDK packages
RUN yes | /sdk/cmdline-tools/latest/bin/sdkmanager --licenses && \
    /sdk/cmdline-tools/latest/bin/sdkmanager "platform-tools" "emulator" "platforms;android-30" "system-images;android-30;default;x86_64"

# RUN echo "no" | /sdk/cmdline-tools/latest/bin/avdmanager create avd -n test -k "system-images;android-30;default;x86_64" && \
#     /sdk/emulator/emulator -avd test -no-window -no-audio &


# Create an AVD
# RUN echo "no" | /sdk/cmdline-tools/latest/bin/avdmanager create avd -n test -k "system-images;android-30;default;x86_64" && \
#     echo "no" | /sdk/cmdline-tools/latest/bin/avdmanager create avd -n test -k "system-images;android-30;default;x86_64" --force

RUN echo "no" | /sdk/cmdline-tools/latest/bin/avdmanager create avd -n test -k "system-images;android-30;default;x86_64" --force

# Verify adb installation
RUN /sdk/platform-tools/adb version

# Set environment variables
# ENV PATH $ANDROID_HOME/cmdline-tools/bin:$PATH
# ENV ANDROID_HOME /sdk
# ENV PATH=$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools


# Install SDK packages and Emulator
# RUN yes | sdkmanager --licenses && \
# sdkmanager "platform-tools" "platforms;android-30" "emulator" "system-images;android-30;google_apis;x86_64"

# Create an Android AVD
# RUN echo "no" | avdmanager create avd -n test_avd -k "system-images;android-30;google_apis;x86_64" -d pixel
# Create and start an Android emulator


# Copy the emulator start script to the container
COPY start-emulator.sh /start-emulator.sh

# Make the script executable
RUN chmod +x /start-emulator.sh

# Run the script (if needed during build)
RUN /start-emulator.sh

# Check if the emulator is running and available
RUN /sdk/platform-tools/adb devices
RUN /sdk/platform-tools/adb shell getprop sys.boot_completed

# Copy the APK and install it
COPY myFawry.apk /myFawry.apk
# RUN /sdk/platform-tools/adb install /myFawry.apk
RUN /sdk/platform-tools/adb devices # Check if adb can see the device
RUN /sdk/platform-tools/adb install /myFawry.apk || (echo "Failed to install APK" && exit 1)


# RUN adb install /myFawry.apk

EXPOSE 4723 5554 5555
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
CMD ["sh", "-c","/start-emulator.sh", "appium & streamlit run Streamlit_view.py", "--server.address=192.168.56.1","--server.port=8501"]


