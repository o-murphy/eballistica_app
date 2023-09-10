# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to prevent interaction during installation
ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd" \
    # SRC_DIR="${HOME_DIR}/src" \  # Using if buildoser sources loaded localy
    PATH="${HOME_DIR}/.local/bin:${PATH}"

# configures locale
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# Update the package lists and install necessary packages
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y \
    autoconf \
    automake \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libssl-dev \
    libtool \
    openjdk-17-jdk \
    patch \
    pkg-config \
    python3-pip \
    python3-setuptools \
    sudo \
    unzip \
    zip \
    zlib1g-dev

# prepares non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Create a directory for linking local files
USER ${USER}
WORKDIR ${WORK_DIR}
# COPY --chown=user:user . ${SRC_DIR}  # Using if buildoser sources loaded localy

# Install buildozer and dependencies
RUN pip3 install --user --upgrade Cython==0.29.36 wheel pip virtualenv buildozer

# Set the entry point to buildozer
ENTRYPOINT ["buildozer"]
