FROM python:3.8-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY SWARM/mysql_api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY MySQL_API/ .
COPY SWARM/config.py .
CMD [ "python", "run.py" ]
