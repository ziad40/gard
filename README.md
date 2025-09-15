# Gard Inventory Management System
https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white
Gard is an inventory management system built with FastAPI, SQLModel, and MySQL. It allows branches to manage categories, products, and inventory processes, with history tracking and media uploads.

## Features

- Branch authentication and registration
- Category and product management with custom ordering
- Inventory process tracking (start, continue, finish)
- History of inventory operations
- Media upload and retrieval for product images
- RESTful API with OpenAPI docs

## Development Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/gard.git
   cd gard
   ```

2. **Create and configure `.env` file**
   ```
   MYSQL_USER=youruser
   MYSQL_PASSWORD=yourpassword
   MYSQL_HOST=db
   MYSQL_PORT=3306
   MYSQL_DB=garddb
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   UPLOADS=/uploads
   BASE_URL=http://localhost:8000/
   ```

3. **Build and run with Docker Compose**
   ```sh
   docker-compose up --build
   ```

4. **Access API docs**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

- [`app/`](app): FastAPI application code
  - [`model/`](app/model): SQLModel ORM models
  - [`routers/`](app/routers): API endpoints
  - [`service/`](app/service): Business logic
  - [`main.py`](app/main.py): App entrypoint
  - [`dependencies.py`](app/dependencies.py): Dependency injection
- [`uploads/`](uploads): Uploaded product images
- [`Dockerfile`](Dockerfile): Container build instructions
- [`docker-compose.yml`](docker-compose.yml): Multi-service orchestration
- [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml): CI/CD workflow for deployment

## Production Deployment

1. **Configure server and secrets**
   - Generate SSH keys and add them to your server and GitHub secrets as described in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

2. **Push to `main` branch**
   - The GitHub Actions workflow will deploy your code to the server, rebuild containers, and restart the app.

3. **Persistent uploads**
   - The `uploads` folder is mounted as a Docker volume for persistent media storage.

## API Workflow

1. **Login/Register branch**
2. **Manage categories and products**
3. **Start and process inventory**
4. **View history and continue unfinished inventories**
5. **Upload and fetch product images**

---

For more details, see the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
