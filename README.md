# App DevOps Project

A simple social network backend built with Django and Django REST Framework. This repository contains the application code; deployment and infrastructure configuration are maintained in the companion repository.

## Live Demo

> **Deployment period:** This project was available online until **October 10, 2026**. The links below are historical deployment addresses and may no longer be accessible.

- **API / Swagger documentation:** https://api.2mohsen.ir
- **Frontend:** https://view.2mohsen.ir

## Related Repository

The application and infrastructure are maintained separately:

- **Application code (this repository):** [2mohsen/app-devops-project](https://github.com/2mohsen/app-devops-project)
- **Deployment and infrastructure:** [2mohsen/infrastructure-devops-project](https://github.com/2mohsen/infrastructure-devops-project)



## How the Projects Work Together

This repository contains the Django application and its API. The infrastructure repository provides the container and deployment configuration used to run the application.

```text
                         Users / API clients
                                  |
                     +------------+------------+
                     |                         |
               Frontend site                API / Swagger
          https://view.2mohsen.ir      https://api.2mohsen.ir
                     |                         |
                     +------------+------------+
                                  |
                         Traefik reverse proxy
                       (infrastructure repository)
                                  |
                         Django application
                       (application repository)
                                  |
                      +-----------+-----------+
                      |                       |
                  PostgreSQL                Redis
```

The infrastructure repository is responsible for packaging and running the application and its supporting services. The application repository is responsible for the backend's business logic and API behavior.

## Main Technologies

- Python
- Django
- Django REST Framework
- JWT authentication
- PostgreSQL
- Redis
- Docker and Docker Compose (deployment configuration is in the infrastructure repository)
- Traefik reverse proxy (infrastructure repository)

## Authentication

The API includes a JWT login endpoint:

```http
POST /api/auth/jwt/login/
```

After authentication, send the access token with requests to protected endpoints:

```http
Authorization: Bearer <access-token>
```

For the current API schema and available endpoints, see the historical API documentation address: https://api.2mohsen.ir

## Repository Responsibilities

### This repository — `app-devops-project`

- Django application code
- API endpoints and routing
- Request handling and validation
- Application models and business logic
- Authentication and authorization

### Companion repository — `infrastructure-devops-project`

- Docker and Docker Compose configuration
- Reverse proxy and routing with Traefik
- Container deployment and networking
- Supporting services and persistent data configuration
- Private image registry configuration with Nexus, where configured

## Project Status

This is a learning and demonstration project. Its hosted deployment was available until **October 10, 2026**. The source code remains available in this repository, but the live services are not guaranteed to be running.

## Links

- [Application repository](https://github.com/2mohsen/app-devops-project)
- [Infrastructure repository](https://github.com/2mohsen/infrastructure-devops-project)
- [API / Swagger](https://api.2mohsen.ir)
- [Frontend](https://view.2mohsen.ir)