
FROM python:3.10


WORKDIR /myapp




COPY requirements.txt .


RUN pip install  -r requirements.txt


COPY . .


EXPOSE 8000
EXPOSE 8001


CMD ["/bin/sh", "-c", "uvicorn Payment.main:app --host 0.0.0.0 --port 8000 & uvicorn Inventory.main:app --host 0.0.0.0 --port 8001 & wait"]