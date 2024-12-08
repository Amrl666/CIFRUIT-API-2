# Gunakan image dasar Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin kode aplikasi
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Jalankan aplikasi
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8080"]
