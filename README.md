# Plantilla de proyecto Django: registro y login de usuarios
Este es un proyecto de Django que se ejecuta en un entorno Docker.

Se trata de una plantilla básica para un proyecto Django, donde ya se ha implementado el registro y el inicio de sesión de usuarios.

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
    docker-compose up --build
    ```
