# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables to prevent interaction during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    libtool git  \
    python3 python3-pip  \
    automake build-essential  \
    openjdk-17-jdk ant \
    unzip

# Install cython, buildozer
RUN pip3 install cython==0.29.36 buildozer

# Create a directory for linking local files
WORKDIR /app

# Copy your local files into the image (assuming your Dockerfile is in the same directory as your local files)
#COPY ./ /app

# docker run -v ./:/app

# Link the .buildozer directory of the image to the local .buildozer directory
#
# Set the entry point to buildozer
ENTRYPOINT ["buildozer"]
