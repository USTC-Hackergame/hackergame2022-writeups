FROM tiangolo/uwsgi-nginx-flask:python3.10

RUN pip install pyOpenSSL==22.0.0 captcha==0.4 gevent==22.8.0
COPY ./app /app
RUN rm -rf /tmp && ln -sf /dev/shm/ /tmp
RUN chmod 0555 /app