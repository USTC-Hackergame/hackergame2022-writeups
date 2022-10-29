FROM tiangolo/uwsgi-nginx-flask:python3.10

# COPY ./requirements.txt /requirements.txt

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install flask qiskit pyOpenSSL matplotlib pylatexenc pycryptodome

COPY ./app /app