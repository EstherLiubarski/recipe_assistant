FROM python:3.12-slim

COPY . ./

WORKDIR /

RUN pip install -r requirements.txt

ENV OPENAI_KEY '<your-openai-api-key>'

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]