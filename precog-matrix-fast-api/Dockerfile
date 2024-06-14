#FROM python:3.10.14-bullseye
FROM python:3.10.6-buster


# Install HDF5 system libraries
#RUN apt-get update && apt-get upgrade -y

#RUN apt-get update && apt-get install -y libhdf5-dev
    #&& apt-get clean \
    #&& rm -rf /var/lib/apt/lists/*

#WORKDIR /app

COPY setup.py setup.py

#COPY requirements.txt /requirements.txt
COPY requirements.txt requirements.txt

COPY app app
#COPY . /app

COPY models models
COPY MANIFEST.in /MANIFEST.in

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

CMD uvicorn app.fast:app --host 0.0.0.0 --port $PORT

# Ensure the ENTRYPOINT is set to your application
#ENTRYPOINT ["python", "app/fast.py"]
