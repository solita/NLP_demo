
# VERSION: 0.1.0
# DESCRIPTION: Basic extensible Python ML development container
# BUILD: docker build --rm -t docker-nlp-python .

# FROM ubuntu:focal-20210827
FROM python:3.9.7-slim-buster

ARG ML_USER="ml_user"
ARG ML_UID="1000"
ARG ML_GID="100"

USER root

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive

# Install usefull stuff
RUN apt-get clean && apt-get update --yes && apt install --yes --no-install-recommends \
    sudo \ 
    locales \
    less \
    htop \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Configure environment
ENV SHELL=/bin/bash \
    ML_USER="${ML_USER}" \
    ML_UID=${ML_UID} \
    ML_GID=${ML_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_CTYPE=en_US.UTF-8 \
    LC_MESSAGES=en_US.UTF-8

ENV HOME="/home/${ML_USER}"
ENV PATH="/home/${ML_USER}/.local/bin:${PATH}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions.sh /usr/local/bin/fix-permissions.sh
RUN chmod a+rx /usr/local/bin/fix-permissions.sh

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${ML_UID}" "${ML_USER}" && \
    chmod g+w /etc/passwd && \
    fix-permissions.sh "${HOME}"

USER $ML_UID

ARG PYTHON_VERSION=default

ENV SHELL=/bin/bash

# Setup work directory for backward-compatibility
RUN mkdir "/home/${ML_USER}/notebooks" && \
    mkdir "/home/${ML_USER}/python" && \
    mkdir "/home/${ML_USER}/work" && \
    fix-permissions.sh "/home/${ML_USER}"

RUN set -ex && fix-permissions.sh "/home/${ML_USER}"

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Expose the port for the Jupyter notebook web interface
EXPOSE 8888

# Expose the port for remote debugging
EXPOSE 3000

WORKDIR "${HOME}"
