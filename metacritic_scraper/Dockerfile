FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY /src .

CMD [ "python", "./main.py" ]
