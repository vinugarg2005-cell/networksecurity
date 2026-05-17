FROM python:3.10-slim-bullseye
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]