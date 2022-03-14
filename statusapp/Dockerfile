FROM python:3.9.10-alpine3.15

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
