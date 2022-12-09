FROM python:3.10

WORKDIR /code

ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip
RUN pip install pip-tools


COPY requirements.in /app/requirements.in
RUN pip-compile /app/requirements.in

RUN pip install -r /app/requirements.txt


COPY . /code

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
