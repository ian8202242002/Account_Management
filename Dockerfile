FROM python:3.9

RUN pip install --upgrade pip

RUN useradd -ms /bin/bash myuser
RUN mkdir -p /account
RUN chown myuser /account
USER myuser
WORKDIR /account

ENV PATH="/home/myuser/.local/bin:${PATH}"

ADD . /account

RUN pip install --user -r requirements.txt

CMD [ "python", "app.py" ]
