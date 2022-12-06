FROM python:3.8-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY k8s/web/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
COPY Web/ .
COPY k8s/config.py .
CMD [ "python", "run.py" ]
