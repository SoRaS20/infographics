

# 🧩 Infographic Generation System — Setup & Run Guide

A FastAPI-based backend that lets users:
- Upload product images & structured data (CSV/JSON)
- Use predefined templates & charts
- Generate static infographic outputs (PNG/PDF)
- Authenticate with JWT
- Store asset metadata in PostgreSQL
- Run locally or in Docker easily

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



## 🧪 Test the Application (via Swagger or Postman)

### 1) Register a User
`POST /auth/register`
```json
{
  "username": "testuser",
  "password": "testpassword"
}
````

Returns: `access_token` (JWT)

---

### 2) Log In

`POST /auth/login` (Form-Data)

```
username = testuser
password = testpassword
```

Copy `access_token`
Use in headers:

```
Authorization: Bearer <token>
```

---

### 3) Upload Assets

* `POST /uploads/image` → upload `.png` or `.jpg` (max 5MB)
* `POST /uploads/data`  → upload `.csv` or `.json` (max 1MB)

**Example CSV**

```csv
product_name,price
Widget,29.99
```

---

### 4) List Available Templates

`GET /templates`
Shows for example: `template1`, `template2`, etc.

---

### 5) Generate Infographic

`POST /generate`

```json
{
  "template": "template1",
  "images": { "product_image": 1 },
  "data_asset_id": 2,
  "charts": [
    {
      "key": "sales_chart",
      "chart_type": "bar",
      "x_col": "product_name",
      "y_col": "price",
      "title": "Product Prices"
    }
  ],
  "format": "png"
}
```

> Replace `1` and `2` with actual `asset_id` values returned from uploads.
> Response = downloadable PNG or PDF.

---

### 6) Stop the Application

```
Ctrl + C     # stop FastAPI server
deactivate   # exit virtual environment
```

### 🧩 API Endpoints

![API Endpoints](outputs/api.png)

The system enables users to upload both an image and structured data (in CSV format). Once uploaded, the data is automatically integrated into a predefined infographic template, generating a polished and visually appealing infographic.

![Generated Infographs](<outputs/infographic (6).png>)
