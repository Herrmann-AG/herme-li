FROM python:3.9.25

LABEL name='pygmy'
LABEL version='1.0.0'
LABEL description='Pygmy(pygy.co) URL shortener'
LABEL vendor="Amit Tripathi"

RUN mkdir /var/log/pygmy

WORKDIR /pygmy

ADD ./requirements.txt /pygmy/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ADD . /pygmy

EXPOSE 8000

CMD ["python3", "run.py"]
