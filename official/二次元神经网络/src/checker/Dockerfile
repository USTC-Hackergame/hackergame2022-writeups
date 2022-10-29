FROM debian:bullseye-slim

# deps
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt update && apt -y upgrade && \
    apt install --no-install-recommends -y python3 python3-pip python3-numpy && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy==1.23.4 matplotlib==3.6.1
RUN pip3 install torch==1.9.1 --extra-index-url https://download.pytorch.org/whl/cpu

RUN rm -rf /tmp && ln -sf /dev/shm/ /tmp
ENV MPLCONFIGDIR=/tmp

COPY server.py /
COPY models.py /
COPY infer.py /
COPY dataset /dataset

CMD ["python3", "/server.py"]
