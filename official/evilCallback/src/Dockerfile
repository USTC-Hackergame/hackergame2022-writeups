FROM ustclug/ubuntu:20.04
# deps
RUN apt update && \
    apt install --no-install-recommends -y python3 gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /tmp/game

# readflag
COPY readflag.c /tmp/readflag.c
RUN gcc /tmp/readflag.c -o /readflag && chmod +s /readflag && \
    rm /tmp/readflag.c && apt remove -y gcc libc6-dev && apt autoremove -y

# chal
COPY ./executable_d8/* /tmp/game/
RUN chmod +x /tmp/game/d8
CMD ["python3", "/tmp/game/s3v3r.py"]
