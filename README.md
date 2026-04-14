
# 🎓 Secure Student Marketplace API

A robust, secure backend prototype for a peer-to-peer student marketplace. This platform allows students to securely upload, sell, and purchase academic notes.

> **Note:** This project focuses on **Backend Security, API Design, and Database Management**. It prioritizes OWASP Top 10 mitigation over UI/UX.

## 🛡️ Security Features
This project implements several critical security measures to ensure a production-grade environment:
*   **Authentication:** JWT (JSON Web Tokens) for stateless authentication.
*   **Password Security:** Passwords are hashed using `bcrypt` (never stored in plain text).
*   **File Upload Security:**
    *   Strict extension whitelisting (`.pdf`, `.png`, `.jpg` only).
    *   Filename sanitization using UUIDs to prevent directory traversal attacks.
    *   Async file handling to prevent memory overflow.
*   **Database Security:** Uses SQLAlchemy ORM to prevent SQL Injection attacks.
*   **Rate Limiting:** Implemented via middleware to prevent Brute Force and DDoS attacks.

## 🚀 Tech Stack
*   **Language:** Python 3.9+
*   **Framework:** FastAPI (High performance, easy validation)
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Authentication:** python-jose (JWT), bcrypt
*   **ASGI Server:** Uvicorn

## 📋 Prerequisites
*   Python 3.9 or higher
*   PostgreSQL (installed and running)

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/secure-marketplace.git
    cd secure-marketplace
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    *   Create a database named `student_marketplace` in your local PostgreSQL instance (pgAdmin or psql).
    *   Update the `SQLALCHEMY_DATABASE_URL` in `app/database.py` with your credentials.

5.  **Run the Server**
    ```bash
    # Install in editable mode to fix module import issues
    pip install -e .
    
    # Start the server
    uvicorn app.main:app --reload
    ```

6.  **Access API Documentation**
    *   Swagger UI: `http://127.0.0.1:8000/docs`
    *   ReDoc: `http://127.0.0.1:8000/redoc`

## 🛣️ API Endpoints

### Authentication
*   `POST /api/auth/register` - Register a new user.
*   `POST /api/auth/login` - Login to receive access token.
*   `GET /api/auth/me` - Get current logged-in user details (Protected).

### Products
*   `POST /api/products/upload` - Upload a new note/product (Protected).
*   `GET /api/products/` - List all available products.
*   `GET /api/products/{id}` - Get details of a specific product.

## 📁 Project Structure
```text
secure-marketplace/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point & CORS config
│   ├── database.py          # DB Connection & Session management
│   ├── models.py            # SQLAlchemy Database Models
│   ├── schemas.py           # Pydantic Schemas for Validation
│   ├── auth.py              # JWT & Password Hashing logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Auth Endpoints
│       └── products.py      # Product & Upload Endpoints
├── uploads/                 # Stored user files
├── requirements.txt
└── README.md
```

## 🔮 Future Scope
*   **Payment Integration:** Stripe Connect for handling seller commissions.
*   **Search & Filter:** Advanced search using PostgreSQL Full-Text Search.
*   **Admin Panel:** Dedicated endpoints for Admins to approve/reject uploaded notes.
*   **Frontend:** React.js dashboard for buyers and sellers.

## 👨‍💻 Author
**Prathamesh Anand**
Backend Enthusiast*
