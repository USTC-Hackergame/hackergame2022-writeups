FROM debian:bullseye-slim

# deps
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt update && apt -y upgrade && \
    apt install --no-install-recommends -y wine wine64 python3 gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# readflag
COPY readflag.c /tmp/readflag.c
RUN gcc /tmp/readflag.c -o /readflag && chmod +s /readflag && \
    rm /tmp/readflag.c && apt remove -y gcc libc6-dev && apt autoremove -y

# wine configuration
RUN WINEPREFIX=/wine/ winecfg && rm /wine/dosdevices/z: && \
    rm /wine/dosdevices/c\:/windows/system32/start.exe && \
    rm /wine/dosdevices/c\:/windows/system32/cmd.exe && \
    rm /wine/dosdevices/c\:/windows/system32/winebrowser.exe && \
    rm /wine/dosdevices/c\:/windows/system32/wineconsole.exe && \
    rm /wine/dosdevices/c\:/windows/system32/winedbg.exe && \
    rm /wine/dosdevices/c\:/windows/system32/winepath.exe && \
    chown -R nobody:root /wine

# container tmpfs -> /dev/shm
RUN rm -rf /tmp && ln -sf /dev/shm/ /tmp

COPY server.py /

CMD ["python3", "/server.py"]
# CMD ["sleep", "1d"]
