[![Pytest](https://github.com/danipineiro/taxi-django-channels/actions/workflows/pytest.yml/badge.svg)](https://github.com/danipineiro/taxi-django-channels/actions/workflows/pytest.yml)

# Integración en tiempo real con Django Channels y Angular
Este proyecto demuestra una integración básica de Django Channels con Angular para mostrar habilidades en la implementación de websockets y comunicación en tiempo real

## Requisitos

- Docker
- Docker Compose

## Configuración inicial

1. Copia el archivo `.env.example` a `.env` y actualiza las variables de entorno según sea necesario.
    ```bash
    cp .env.example .env
    ```
   
2. Construye y levanta los servicios de Docker.
    ```bash
    docker compose up --build
    ```
