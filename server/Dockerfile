FROM python:3.6

WORKDIR /server

COPY requirements.txt /server/requirements.txt
RUN pip install -r requirements.txt

COPY config /root/.kube/config
COPY server.py /server/server.py
COPY kube.py /server/kube.py

ENV FLASK_ENV=development
ENV FLASK_APP=server.py

EXPOSE 5000

CMD ["flask" , "run", "--host=0.0.0.0"]
#CMD ["python" , "server.py"]
