

# FastAPI Professional Template

Modern, production-ready FastAPI template with Dual DB Support (Sync/Async), SQL Alchemy 2.0, and automated logging.

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/alejandrofonsecacuza/FastAPI-Professional-Template.git fastapi_template
cd fastapi_template

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Configuration

```bash
# Copy template environment variables
cp .env.example .env

# Edit .env with your database credentials
nano .env

```

### 3. Run the Application

```bash
python3 main.py

```

> The API will be available at `http://localhost:8000`
> Interactive docs: `http://localhost:8000/docs`

---

## 📂 Project Structure

* **`app/api/`**: API routes and dependencies.
* **`app/core/`**: Config, Database (Sync/Async), and Logger.
* **`app/models/`**: SQLAlchemy ORM models.
* **`app/schemas/`**: Pydantic validation models.
* **`app/services/`**: Business logic.
* **`logs/`**: Automated rotating log files.

## ⚙️ Features

* **Dual DB Session**: `AsyncSession` for FastAPI and `Session` for background tasks (Celery).
* **Auto-Rotation Logs**: 10MB limit with 5 backup files.
* **Lifespan Management**: Handles DB connection retries on startup.

