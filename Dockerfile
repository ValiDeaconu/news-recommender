FROM python:3.9.7

WORKDIR /app

COPY ./server ./server
COPY ./app.py ./app.py
COPY ./db.py ./db.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

CMD ["python", "./app.py"]