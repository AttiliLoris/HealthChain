FROM python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copia il tuo script nel container
COPY acceptLicense.py .
COPY findCoordinates.py .
# Copia le immagini di riferimento nel container


#dobbiamo scegliere la nostra directory per ora è HealthChain
WORKDIR /HealthChain
COPY . /HealthChain

#pure qui possiamo lasciare o cambiare
EXPOSE 8000

#qui dobbiamo far partire il nostro progetto quindi ad esempio ora sarebbe HealthChain/offChain/main.py
CMD [ "python", "/HealthChain/offChain/main.py" ]
