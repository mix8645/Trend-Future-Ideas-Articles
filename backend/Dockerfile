FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# 3. Install Python libraries
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application files
COPY --chown=user . .

# 5. Expose port
EXPOSE 7860

# 6. Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]