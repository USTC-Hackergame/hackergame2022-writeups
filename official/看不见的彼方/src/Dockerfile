FROM debian:bullseye-slim

# deps
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt update && apt -y upgrade && \
    apt install --no-install-recommends -y python3 libseccomp-dev gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# executor
COPY executor.c /tmp/executor.c
RUN gcc /tmp/executor.c -o /executor -lseccomp && \
    rm /tmp/executor.c && apt remove -y gcc libc6-dev libseccomp-dev && apt autoremove -y

# user
RUN useradd -m pwn && mkdir /home/pwn/A && mkdir /home/pwn/B && \
    cp -r /lib* /home/pwn/A/ && cp -r /lib* /home/pwn/B/ && \
    mkdir /home/pwn/A/usr && mkdir /home/pwn/B/usr && \
    cp -r /usr/lib* /home/pwn/A/usr/ && cp -r /usr/lib* /home/pwn/B/usr/ && \
    mkdir /home/pwn/A/bin && mkdir /home/pwn/B/bin && \
    cp /bin/sh /bin/cat /bin/ls /home/pwn/A/bin && cp /bin/sh /bin/cat /bin/ls /home/pwn/B/bin && \
    cp /executor /home/pwn/A/ && cp /executor /home/pwn/B/ && \
    chmod -R 555 /home/pwn

COPY server.py /

CMD ["python3", "-u", "/server.py"]
