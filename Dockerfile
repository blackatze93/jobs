FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip
RUN pip install pip-tools


COPY requirements.in /app/requirements.in
RUN pip-compile /app/requirements.in

RUN pip install -r /app/requirements.txt


COPY . /app

EXPOSE 8000
CMD ["python", "main.py"]