FROM python:3.10.10-slim-bullseye

WORKDIR /app

COPY ./src ./src

CMD [ "python", "./src/main.py" ]

# CMD [ "python3", "./main.py" ]
