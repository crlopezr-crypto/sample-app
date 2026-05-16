#!/bin/bash

# -- Crear estructura de directorios --
mkdir tempdir

# -- Copiar archivos de la app --
cp app.py tempdir/.
cp requirements.txt tempdir/.

# -- Crear Dockerfile con echo --
echo "FROM python:3.11-slim" > tempdir/Dockerfile
echo "WORKDIR /app" >> tempdir/Dockerfile
echo "COPY requirements.txt ." >> tempdir/Dockerfile
echo "RUN pip install --no-cache-dir -r requirements.txt" >> tempdir/Dockerfile
echo "COPY app.py ." >> tempdir/Dockerfile
echo "ENV BASE_URL=https://restcountries.com/v3.1" >> tempdir/Dockerfile
echo "ENV TIMEOUT=10" >> tempdir/Dockerfile
echo "CMD [\"python\", \"-u\", \"app.py\"]" >> tempdir/Dockerfile

# -- Build y Run --
cd tempdir
docker build -t geoops-intelligence .
docker run -it --name samplerunning geoops-intelligence
docker ps -a
