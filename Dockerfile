FROM python:3.7-slim
WORKDIR /app

# Install system libraries
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y gcc

# Install project dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Don't use terminal buffering, print all to stdout / err right away
ENV PYTHONUNBUFFERED 1

COPY . .
CMD ["python", "app.py"]