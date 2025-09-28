# URL Shortener

**URL Shortener** service built with **FastAPI**, **MySQL**, and **Hexagonal Architecture**.  

---

## 📂 Project Structure

```
src/
├── domain/              # Entities, domain services, repository interfaces
├── application/         # Application services (use cases)
├── infrastructure/      # Adapters (MySQL repo, logging, FastAPI entrypoints)
├── main.py              # FastAPI app entrypoint
tests/                   # Unit & integration tests
docker-compose.yml       # App + MySQL setup
.env                     # Environment variables
```

---

## ⚙️ Requirements

- Docker & Docker Compose
- Python 3.11+ (if running locally without Docker)

---

## 🚀 Running the App

1. **Set up environment variables** in `.env`:

```env
MYSQL_ROOT_PASSWORD=root
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=appuser
MYSQL_PASSWORD=apppass
MYSQL_DATABASE=url_shortener
MYSQL_POOL_MIN=1
MYSQL_POOL_MAX=10
DB_PORT=3306

APP_DEBUG_LEVEL=DEBUG
APP_NAME="url-shortener"
```

2. **Start the services**:

```bash
docker compose build
```

Start the database first:
```bash
docker compose up db
```

Then the app in a different terminal:
```bash
docker compose up app
```

3. Access the API at:  
👉 [http://localhost:8000](http://localhost:8000)

---

## 🛠 Example Usage

**Shorten a URL:**
```bash
curl -X POST http://localhost:8000/urls \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.lemonde.fr/robots.txt"}'
```

**Response:**
```json
{
    "short_code":"c61155",
    "original_url":"https://www.lemonde.fr/robots.txt"
}
```

**Retrieve original URL:**

```bash
curl -i http://localhost:8000/c61155 
```

```bash
HTTP/1.1 307 Temporary Redirect
date: Sun, 28 Sep 2025 20:01:50 GMT
server: uvicorn
content-length: 0
location: https://www.lemonde.fr/robots.tx
```

**Retrieve original URL and redirect**

```bash
curl -L http://localhost:8000/c61155 
```
