FROM python:3.11-bullseye

# Install dependencies untuk rembg & Pillow
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies (versi aman & stabil)
RUN pip install --no-cache-dir \
    flask gunicorn gevent rembg pillow onnxruntime==1.14.1

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-k", "gevent", "--worker-connections", "100", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
