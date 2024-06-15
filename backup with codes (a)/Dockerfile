FROM python:3.10.14-bullseye
#FROM python:3.10.6-buster

# Install HDF5 system libraries
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY setup.py setup.py

#COPY requirements.txt /requirements.txt
COPY requirements.txt requirements.txt
COPY API /app
COPY utils /utils
COPY models /models
COPY MANIFEST.in /MANIFEST.in

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn app.fast:app --host 0.0.0.0 --port $PORT
