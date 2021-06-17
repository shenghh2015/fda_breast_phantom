FROM nvidia/cuda:11.0-runtime-ubuntu16.04

# Python 2.7 or 3.5 is supported by Ubuntu Xenial out of the box
#ARG python=2.7
ENV PYTHON_VERSION=2.7

# enables the container to interact with the “System Security Services Daemon” (sssd) on the execution host (washU compute1)
RUN apt-get update \
  && apt-get install -y libnss-sss \
  && apt-get clean all \
  && rm -r /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
	python${PYTHON_VERSION} \
	python${PYTHON_VERSION}-dev

#RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python

RUN apt-get update&& apt-get install cuda-samples-10-2 -y

RUN apt-get install -y \
        cmake apt-utils vtk6 libvtk6-dev \
        libblas-dev liblapack-dev \
        libboost-dev libboost-program-options-dev \
        libproj-dev libtet1.5-dev zlib1g-dev \
        python-numpy python-scipy vim

WORKDIR /scratch
COPY ./scratch /scratch

WORKDIR /data

## Xray imaging
RUN apt-get install -y \
    wget alien software-properties-common

# install open mpi
RUN cd /scratch &&\
    wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-3.1.5-1.src.rpm &&\
    alien openmpi-3.1.5-1.src.rpm &&\
    rm openmpi-3.1.5-1.src.*

RUN cd /scratch/04-VICTRE_MCGPU &&\
    sh make_MC-GPU_v1.5b.sh
