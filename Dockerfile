FROM python:3.10-slim-buster

WORKDIR /app
COPY . .

RUN python3 -m pip install -r requirements.txt
CMD python3 installer.py --nointeract && python3 src/main.py
