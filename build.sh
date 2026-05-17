#!/bin/bash

# -- Crear estructura de directorios --
rm -rf tempdir
docker rm -f samplerunning 2>/dev/null || true
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
echo "ENV AUTO_MODE=1" >> tempdir/Dockerfile
echo "CMD [\"python\", \"-u\", \"app.py\"]" >> tempdir/Dockerfile

# -- Build y Run --
cd tempdir
docker build -t geoops-intelligence .
docker run --name samplerunning -e AUTO_MODE=1 geoops-intelligence
docker build --no-cache -t geoops-intelligence .
docker ps -a
