# Use Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install font dependencies
RUN mkdir -p /usr/share/fonts/truetype/ttf && \
    wget -q -O /usr/share/fonts/truetype/ttf/Vazir.ttf https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazir.ttf && \
    wget -q -O /usr/share/fonts/truetype/ttf/Vazirmatn-Bold.ttf https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/Vazir-Bold.ttf

# Install pip and dependencies
RUN pip install --upgrade pip setuptools && pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Django will run on
EXPOSE 8000

# Define command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]