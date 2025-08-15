FROM python:3.11-slim
RUN pip install psutil colorama
COPY spy.py /app/spy.ru
WORKDIR /app
CMD ["python3", "spy.py"]
