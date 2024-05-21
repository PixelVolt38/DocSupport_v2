# Usa una imagen base que contenga el sistema operativo que deseas
#FROM ubuntu:latest
#
## Actualiza los repositorios e instala GCC
#RUN apt-get update && \
#    apt-get install -y gcc
#
# Usar la imagen base oficial de Python 3.12 slim
FROM python:3.11-slim

# Exponer el puerto que usará Streamlit
EXPOSE 8080

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar todos los archivos del proyecto al contenedor
COPY . ./

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade --user google-cloud-aiplatform
RUN pip3 install -U 'anthropic[vertex]'
RUN pip install -U langchain-community

# Comando para ejecutar la aplicación de Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
