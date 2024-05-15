FROM python:3.12-slim
EXPOSE 8080
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
RUN pip3 install --upgrade --user google-cloud-aiplatform
RUN pip3 install -U 'anthropic[vertex]'
RUN pip install -U langchain-community
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]