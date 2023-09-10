# Use the official Ubuntu base image
FROM omurphyslaw/buildozer:test

# Update the package lists and install necessary packages
RUN sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y wget

# Download and install Apache Ant 1.9.4
RUN wget https://archive.apache.org/dist/ant/binaries/apache-ant-1.9.4-bin.tar.gz -O apache-ant.tar.gz && \
    sudo tar xzf apache-ant.tar.gz -C /opt && \
    rm apache-ant.tar.gz

# Set environment variables for Apache Ant
ENV ANT_HOME=/opt/apache-ant-1.9.4
ENV PATH="${ANT_HOME}/bin:${PATH}"

# Download and install Android SDK command-line tools
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip -O android-sdk.zip && \
    unzip android-sdk.zip -d ${HOME_DIR}/android-sdk && \
    rm android-sdk.zip

# Set environment variables for Android SDK
ENV ANDROID_SDK_ROOT=${HOME_DIR}/android-sdk
ENV PATH="${ANDROID_SDK_ROOT}/tools/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}"

# Accept Android SDK licenses
# RUN yes | sdkmanager --licenses
# RUN ls "${ANDROID_SDK_ROOT}/tools/bin"
# RUN echo "ANDROID_SDK_ROOT: $ANDROID_SDK_ROOT"
# RUN echo "PATH: $PATH"
# RUN sdkmanager --update
# RUN yes | sdkmanager --licenses


# Download and install Android NDK 25b
RUN wget https://dl.google.com/android/repository/android-ndk-r25b-linux.zip -O android-ndk.zip && \
    unzip android-ndk.zip -d ${HOME_DIR} && \
    rm android-ndk.zip

# Set environment variables for Android NDK
ENV ANDROID_NDK_HOME=${HOME_DIR}/android-ndk-r25b
ENV PATH="${ANDROID_NDK_HOME}:${PATH}"

# Set the entry point to buildozer
ENTRYPOINT ["buildozer"]
