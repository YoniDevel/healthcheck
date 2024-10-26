FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade /code/requirements.txt

COPY ./src /code/src

CMD [ "py", "src/main.py" ]
