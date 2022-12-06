FROM python:3.8-slim
WORKDIR /app

RUN python -m pip install --upgrade pip
COPY k8s/iot_api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY IoT_API/ .
COPY k8s/config.py .
CMD [ "python", "run.py" ]
