[![Pytest](https://github.com/danipineiro/taxi-django-channels/actions/workflows/pytest.yml/badge.svg)](https://github.com/danipineiro/taxi-django-channels/actions/workflows/pytest.yml)

# Proyecto: Integración en Tiempo Real con Django Channels y Angular

Este proyecto es una demostración de habilidades en el uso de **Django Channels** para la comunicación en tiempo real junto a **Angular** como frontend. Además, el proyecto se despliega con **Docker** para simplificar la configuración y ejecución.

---

## Descripción
La finalidad de este proyecto es ilustrar la integración de **Django Channels** y **Angular** en un entorno de comunicación en tiempo real utilizando websockets, ideal para demostrar competencia en estas tecnologías para un portfolio.

## Características

- **Comunicación en tiempo real**: Implementación de websockets con Django Channels.
- **Actualización instantánea**: Actualización automática de datos en el frontend.
- **Despliegue con Docker**: Facilidad de despliegue y gestión del entorno.

## Tecnologías Utilizadas

- **Backend**: Django, Django Rest Framework, Django Channels, Redis
- **Frontend**: Angular
- **Librería UI**: Angular Material
- **Contenerización**: Docker y Docker Compose

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

3. Accede a la aplicación en [http://localhost:4200](http://localhost:4200).
