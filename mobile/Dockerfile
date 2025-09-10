FROM node:22-alpine

RUN apk add --no-cache \
    git \
    python3 \
    make \
    g++ \
    openjdk11-jdk \
    android-tools \
    wget \
    curl

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV ANDROID_HOME=/usr/local/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

WORKDIR /app

RUN corepack enable pnpm

# Copiar archivos de configuración del package
COPY aplicacion/package.json aplicacion/pnpm-lock.yaml ./

# Instalar dependencias
RUN pnpm install --frozen-lockfile

# Instalar herramientas globales
RUN npm install -g @ionic/cli @capacitor/cli

# Copiar TODOS los archivos de configuración (incluyendo tsconfig.node.json)
COPY aplicacion/ionic.config.json \
     aplicacion/capacitor.config.ts \
     aplicacion/tsconfig.json \
     aplicacion/tsconfig.node.json \
     aplicacion/vite.config.ts \
     aplicacion/index.html ./

# Copiar código fuente
COPY aplicacion/src ./src
COPY aplicacion/public ./public

# Crear usuario
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 8100

CMD ["ionic", "serve", "--host", "0.0.0.0", "--port", "8100", "--no-open", "--livereload"]