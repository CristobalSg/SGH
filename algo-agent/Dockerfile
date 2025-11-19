FROM debian AS fet-builder

WORKDIR /fet

COPY ./fet-7.5.5/ .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libice6 \
    libxtst6 \
    libnss3 \
    libx11-xcb1 \
    libxcb1 \
    libxau6 \
    libxdmcp6 \
    && rm -rf /var/lib/apt/lists/*

RUN qmake fet.pro && \
    make -j 16 && \
    cp fet-cl /usr/bin/fet-cl

FROM python:3.12-slim AS app-runner

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

COPY . .

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8200

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port" , "8200"]