FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# RUN chmod +x /app/docker/*.sh
WORKDIR src

CMD [ "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000" ]