# Usa una imagen base que contenga el sistema operativo que deseas
FROM ubuntu:latest

# Actualiza los repositorios e instala GCC
RUN apt-get update && \
    apt-get install -y gcc
    
FROM python:3.12-slim
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
RUN pip3 install --upgrade --user google-cloud-aiplatform
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]