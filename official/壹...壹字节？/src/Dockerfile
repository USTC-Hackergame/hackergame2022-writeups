FROM debian:latest
RUN apt update && apt -y upgrade && \
    apt install -y --no-install-recommends qemu-system 

RUN useradd -m -s /bin/bash ctf

COPY pwn/ /home/ctf/

CMD ["/home/ctf/scripts/run.sh"]