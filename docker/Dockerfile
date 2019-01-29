# Docker image for VFRAME workshop
# https://github.com/vframeio/vframe_workshop

FROM continuumio/anaconda3
MAINTAINER Adam Harvey / VFRAME

ENV DEBIAN_FRONTEND noninteractive

# [ apt ]

RUN apt-get update && \
  apt-get upgrade -y

RUN apt install -y \
	cmake \
	build-essential \
	libgtk-3-dev \
	libboost-all-dev \
	youtube-dl


# [ conda environments ]

ADD environment.yml /tmp/environment.yml
RUN conda env create -f tmp/environment.yml


# [ docker permissions/user ]

ENV DOCKER_USER docker
RUN useradd -d /home/${DOCKER_USER} -ms /bin/bash -g root -G sudo -p ${DOCKER_USER} ${DOCKER_USER}

# [ zsh ]

RUN apt install -y zsh 
RUN git clone git://github.com/robbyrussell/oh-my-zsh.git /root/.oh-my-zsh
RUN cp /root/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
RUN chsh -s /bin/zsh

WORKDIR /home/${DOCKER_USER}

ENTRYPOINT /vframe_workshop/docker/entrypoint.sh