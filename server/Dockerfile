FROM python:3.6

RUN pip install kubernetes
WORKDIR /server

COPY config /root/.kube/config
COPY server.py /server/server.py

CMD ["python","server.py"]