FROM python:3.7.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
CMD ["python", "scanner/networks/networks_scan_entrypoint.py"]
