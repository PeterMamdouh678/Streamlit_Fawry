FROM python
WORKDIR /Deploy

# Set environment variables to avoid buffering and output issues
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     DEBIAN_FRONTEND=noninteractive

COPY . /Deploy
# Install system dependencies
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g appium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         apt-transport-https \
#         ca-certificates \
#         openjdk-11-jdk \
#         curl \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Appium)
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN appium driver install uiautomator2


# Install Appium globally
# RUN npm install -g appium

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4723
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health


# CMD ["streamlit", "run", "Streamlit_view.py"]
# CMD ["streamlit", "run", "Streamlit_view.py", "--server.port=8501", "--server.enableCORS=false"]

# CMD ["sh", "-c", "appium & streamlit run Streamlit_view.py"]
CMD ["sh", "-c", "appium & streamlit run Streamlit_view.py", "--server.address=192.168.56.1","--server.port=8501"]

# CMD ["streamlit","run","Streamlit_view.py"]




# import subprocess

# def get_emulator_device_name():
# # Execute the adb devices command to list all connected devices
# result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE)
# output = result.stdout.decode("utf-8")

# # Extract device names (usually the first column in the output)
# device_lines = output.strip().split('\n')[1:] # Skip the first line 'List of devices attached'
# devices = [line.split()[0] for line in device_lines if "emulator" in line]

# # Return the list of emulator device names
# return devices

# if __name__ == "__main__":
# emulator_devices = get_emulator_device_name()
# if emulator_devices:
# print("Emulator devices found:")
# for device in emulator_devices:
# print(device)
# else:
# print("No emulator devices found.")
