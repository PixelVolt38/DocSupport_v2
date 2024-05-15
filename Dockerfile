FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
FROM python:3.12-slim
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
RUN pip3 install --upgrade --user google-cloud-aiplatform
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]