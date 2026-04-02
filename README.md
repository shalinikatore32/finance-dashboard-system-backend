# 📊 Finance Dashboard API

A modular, production-ready backend designed to power a robust Finance Dashboard. Built using modern Python principles with **FastAPI**, **MongoDB Atlas**, and **Motor (Async)**.

---

## 🏛 1. Backend Design & Architecture
This application strictly adheres to the **Separation of Concerns** principle.
- **`routers/`**: Pure HTTP delivery layer. Only handles receiving requests and returning HTTP responses.
- **`services/`**: The core business logic. All database querying, aggregations, and data manipulations live here.
- **`models/` & `schemas/`**: Strict Pydantic v2 schemas validating incoming payloads and serializing outgoing database responses.
- **`core/` & `db/`**: Reusable configuration, JWT security, and singleton database connection handlers.

## 🧠 2. Logical Thinking & Access Control
We utilize **FastAPI Dependencies** to inject Role-Based Access Control (RBAC) securely into routes:
- **`Viewer`**: Can view lists of generic transactions (Read-Only).
- **`Analyst`**: Can view transactions AND access complex Dashboard Summary aggregations.
- **`Admin`**: Full CRUD. Authorized to create users, update roles, and manage transactions directly.

## 🗄 3. Database & Data Modeling
- **MongoDB** was selected due to its flexibility with unstructured transaction data (like open-ended `notes`) and high performance with complex dashboard aggregations (`$group`, `$match`).
- **Id Mapping**: Pydantic v2 handles safely mapping MongoDB's `ObjectId('_id')` automatically to a JSON-serializable `id` string for the frontend.

## 🛡️ 4. Validation & Reliability
- **Pydantic Schemas**: Guarantees input validation (e.g., negative money amounts reject with a 422, strict email string types).
- **Global Error Handling**: Custom middleware specifically intercepts `RateLimitExceeded`, `ValueError`, and `HTTPExceptions` to return elegant, predictable JSON error contracts to the frontend.

## 🏗️ 5. Assumptions & Tradeoffs
- **Assumption**: We assume usernames will just be user emails to streamline login.
- **Assumption**: Since transactions drive analytics, we favor **Soft Deletes**.
- **Tradeoff**: We use `Motor` for asynchronous database connections. While it is significantly more performant than standard PyMongo under high load, it requires tight governance of `async/await` syntax throughout the application.

## 🚀 6. Additional Thoughtfulness (Enhancements Built)
- **Advanced Pagination & Searching**: Implemented `page`, `limit`, and keyword `regex` searching natively on the `GET /transactions` endpoint.
- **Soft Delete Architecture**: Transactions are never hard-destroyed, protecting historical accounting.
- **Rate-Limiting Throttling**: Embedded `slowapi` restricts routes to 100 requests/minute per IP to defend against API abuse.
- **Containerization Readiness**: Included a lightweight `Dockerfile` and `docker-compose.yml` for instant, environment-agnostic deployment.
- **Automated Testing**: Integrated `pytest` leveraging `pytest-asyncio` for ensuring core health and auth routes resist regressions.

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- A MongoDB instance (or Atlas Cluster string)

### 1. Installation
```bash
python -m venv venv
# Activate your venv: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Open the `.env` file and replace `MONGODB_URL` with your MongoDB Atlas connection string.

### 3. Seed Initial Data
```bash
python seed.py
```
*(This scripts automatically purges the DB and creates dummy transactions alongside your Admin, Analyst, and Viewer dummy accounts).*

### 4. Run the API Server
```bash
uvicorn app.main:app --reload
```

Interactive Swagger Documentation will immediately become available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.
