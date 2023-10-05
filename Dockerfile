FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

COPY aaa.txt .

CMD ["python", "-u", "main.py"]
