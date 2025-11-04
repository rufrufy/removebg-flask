FROM python:3.11-slim

# Tambahkan library sistem yang dibutuhkan
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 libmagic1 execstack \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install dependency Python (gunakan versi stabil onnxruntime)
RUN pip install --no-cache-dir \
    flask gunicorn gevent rembg pillow onnxruntime==1.14.1

# Perbaiki permission eksekusi stack agar tidak error
RUN find /usr/local/lib/python3.11/site-packages/onnxruntime/ -name "*.so" -exec execstack -c {} \; || true

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-k", "gevent", "--worker-connections", "100", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
