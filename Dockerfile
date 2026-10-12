FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["python", "-m", "streamlit", "run", "src/careerpilot/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
