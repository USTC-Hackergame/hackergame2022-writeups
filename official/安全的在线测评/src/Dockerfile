FROM python:3
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list &&\
    apt update && apt -y upgrade && \
    apt install -y gcc=4:10.2.1-1 python3 gosu && \
    rm -rf /var/lib/apt/lists/*
RUN pip install sympy
RUN groupadd -r judger && useradd -r -g judger judger && \
    groupadd -r runner && useradd -r -g runner runner&& \
    passwd --delete runner
WORKDIR /judger
RUN mkdir -m 777 /judger/temp
COPY --chown=judger checker.py ./
COPY --chown=judger flag.py ./
COPY --chown=judger run.sh ./
COPY --chown=judger data ./data

# --tmpfs /dev/shm:exec is required when running in docker
CMD ["./run.sh"]
