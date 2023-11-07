FROM python:3.10.6-slim-buster

WORKDIR /app
COPY app.py app.py
COPY assets/ assets/
COPY pages/ pages/
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
