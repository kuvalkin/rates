FROM python:3.11

WORKDIR /app

COPY requirments.txt .

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]