FROM python:3.9-slim
WORKDIR /youtube-fetcher
COPY . /youtube-fetcher
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
