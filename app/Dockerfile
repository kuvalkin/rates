FROM python:3.11

WORKDIR /app

COPY requirments.txt .

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

RUN pip install -e .

CMD ["python", "-m", "flask", "--app", "src/app/app.py", "run", "--host=0.0.0.0"]