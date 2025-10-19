

# 🧩 Infographic Generation System — Setup & Run Guide



## 🚀 — Run Locally 

### 1) Prerequisites

- Python 3.11+  
- PostgreSQL running locally  
- Required folders exist:
  ```bash
  mkdir -p uploads/images uploads/data


### 2) Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure `.env`

Create `.env` in project root:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/infographics
UPLOAD_DIR=./uploads
```

Generate a secret key if needed:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5) Setup PostgreSQL Database

```bash
createdb infographics
# OR
psql -U username -c "CREATE DATABASE infographics;"
```

Tables are auto-created on app start.

### 6) Run Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open Swagger:
[http://localhost:8000/docs](http://localhost:8000/docs)

---
