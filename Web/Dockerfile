FROM python:3.8-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY app .
CMD [ "python", "run.py" ]
