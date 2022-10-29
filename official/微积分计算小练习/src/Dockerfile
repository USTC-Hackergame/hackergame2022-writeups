FROM debian:bullseye-slim

COPY bot/requirements.txt /tmp/
RUN apt update && apt install -y --no-install-recommends python3 python3-pip chromium-driver \
    && pip3 install -r /tmp/requirements.txt && rm -rf /var/lib/apt/lists/*

COPY bot /app
WORKDIR /app

ENTRYPOINT ["python3", "-u", "bot.py"]