<div align="center">

# Distributed Secure Notes Application

### Enterprise-Grade Collaborative Note Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-LTS-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-JWT%20%7C%20RBAC-orange)](/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](/)

[Features](#-key-features) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [Documentation](#-documentation) • [Security](#-security) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Security](#-security)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🌟 Overview

The **Distributed Secure Notes Application** is an enterprise-grade, full-stack collaborative note management system designed with security, scalability, and reliability at its core. Built for modern distributed environments, this application demonstrates industry best practices in secure application development, distributed systems architecture, and real-time collaboration.

### Academic Project Highlights

- **Enhanced Security**: Multi-layered security architecture demonstrating secure application development
- **Scalability**: Distributed master-replica architecture showing system design principles
- **Real-time Collaboration**: Concurrent editing with intelligent locking mechanisms
- **Access Control**: Granular permission system implementing role-based access control
- **High Availability**: Fault-tolerant design principles in distributed systems

### Learning Outcomes

- **Secure Application Development**: Implementation of industry-standard security practices
- **Distributed Systems**: Understanding of master-replica architecture and data synchronization
- **Full-Stack Development**: Integration of modern backend and frontend technologies
- **Software Architecture**: Application of design patterns and architectural principles

---

## ✨ Key Features

### 🔐 Security & Authentication

- **JWT-based Authentication**: Stateless, secure token-based authentication system
- **Role-Based Access Control (RBAC)**: Fine-grained permission management
- **Password Security**: Industry-standard bcrypt hashing with salt
- **XSS Protection**: Input sanitization and output encoding
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy ORM
- **Security Headers**: CORS, CSP, X-Frame-Options, and more
- **Session Management**: Secure cookie handling with HTTP-only flags

### 📝 Note Management

- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Visibility Controls**: Private, Read-Only, and Read/Write sharing options
- **Rich Content Support**: Formatted text with XSS-safe rendering
- **Version Tracking**: Automatic timestamps for creation and modification
- **Search & Filter**: Efficient note discovery and organization

### 🔄 Distributed Architecture

- **Master-Replica Synchronization**: Automatic data replication for high availability
- **Concurrency Control**: Optimistic locking mechanism preventing conflicts
- **Load Distribution**: Read queries distributed across replica nodes
- **Fault Tolerance**: Automatic failover and recovery mechanisms
- **Data Consistency**: Eventual consistency model with conflict resolution

### 🤝 Collaboration Features

- **Real-time Locking**: Prevent simultaneous edits with user-aware locks
- **Shared Notes**: Multiple visibility levels for collaborative workflows
- **User Attribution**: Track note ownership and last editor
- **Access Badges**: Visual indicators of permission levels

---

## 🏗 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer (React)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Auth Module │  │ Notes Manager│  │  UI Components│      │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS / REST API
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer (Flask)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   API Routes │  │   Services   │  │ Middleware   │       │
│  │              │  │              │  │ (JWT, CORS)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────┬────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   Master Database       │   │   Replica Database      │
│   (SQLite)              │──▶│   (SQLite)              │
│   - Write Operations    │   │   - Read Operations     │
│   - Data Replication    │   │   - Failover Support    │
└─────────────────────────┘   └─────────────────────────┘
```

### Technology Stack

#### Backend Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | Primary backend language |
| **Flask** | 3.0.x | Web framework and REST API |
| **SQLAlchemy** | 2.0+ | ORM and database abstraction |
| **SQLite** | 3.x | Lightweight relational database |
| **Flask-JWT-Extended** | 4.x | JWT authentication |
| **Flask-CORS** | 4.x | Cross-Origin Resource Sharing |
| **bcrypt** | 4.x | Password hashing |
| **pytest** | 7.x | Testing framework |

#### Frontend Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.x | UI framework |
| **React Router** | 7.x | Client-side routing |
| **JavaScript** | ES6+ | Programming language |
| **HTML5/CSS3** | - | Markup and styling |
| **Fetch API** | - | HTTP client |

#### DevOps & Tools

- **Git** - Version control
- **npm** - Package management
- **pip** - Python package management
- **venv** - Virtual environment management

---

## 🚀 Getting Started

---

## 🚀 Getting Started

### Prerequisites

Ensure the following tools are installed on your system:

| Tool | Version | Installation | Verification |
|------|---------|--------------|--------------|
| **Python** | 3.10+ | [Download](https://www.python.org/downloads/) | `python --version` |
| **Node.js** | LTS (18.x+) | [Download](https://nodejs.org/) | `node --version` |
| **npm** | 9.x+ | Included with Node.js | `npm --version` |
| **SQLite** | 3.x | [Download](https://www.sqlite.org/download.html) | `sqlite3 --version` |
| **Git** | Latest | [Download](https://git-scm.com/) | `git --version` |

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/your-org/distributed-secure-notes.git
cd distributed-secure-notes
```

#### 2. Backend Setup

**Create and activate virtual environment:**

**Windows:**
```batch
cd back
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
cd back
python -m venv .venv
source .venv/bin/activate
```

**Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Frontend Setup

```bash
cd front-app
npm install
```

### Configuration

#### Environment Variables

Create a `.env` file in the `back/` directory:

```env
# Application Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here

# Server Configuration
SERVER_MODE=master  # or 'replica'
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:///instance/notes.db

# Security Configuration
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=http://localhost:3000

# Replica Configuration (if running as replica)
MASTER_URL=http://localhost:5000
```

**Frontend Configuration:**

Update `src/config.js` (create if needed):

```javascript
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export const APP_NAME = 'Secure Notes';
```

---

## 💻 Usage

### Quick Start (Recommended)

Use the provided scripts to start all services simultaneously:

**Windows:**
```batch
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

This will start:
- Master Backend Server (Port 5000)
- Replica Backend Server (Port 5001)
- Frontend Development Server (Port 3000)

### Manual Start

#### Start Master Server

**Windows:**
```batch
cd back
.venv\Scripts\activate
set SERVER_MODE=master
set PORT=5000
python app.py
```

**Linux/macOS:**
```bash
cd back
source .venv/bin/activate
export SERVER_MODE=master
export PORT=5000
python app.py
```

#### Start Replica Server

**Windows:**
```batch
cd back
.venv\Scripts\activate
set SERVER_MODE=replica
set PORT=5001
python app.py
```

**Linux/macOS:**
```bash
cd back
source .venv/bin/activate
export SERVER_MODE=replica
export PORT=5001
python app.py
```

#### Start Frontend

```bash
cd front-app
npm start
```

### Accessing the Application

- **Frontend UI**: http://localhost:3000
- **Master API**: http://localhost:5000/api
- **Replica API**: http://localhost:5001/api

### Default Credentials

For testing purposes (development environment only):

```
Username: alice
Password: password123
```

---

## 🧪 Testing

### Backend Testing

The project includes comprehensive security and functionality tests.

#### Run All Tests

**Windows:**
```batch
cd back
.venv\Scripts\activate
pip install -r test_requirements.txt
python -m pytest tests/ -v
```

**Using provided script:**
```batch
./back/run_tests.bat
```

**Linux/macOS:**
```bash
cd back
source .venv/bin/activate
pip install -r test_requirements.txt
python -m pytest tests/ -v
```

#### Run Specific Test Suites

**Security Tests:**
```bash
python -m pytest tests/test_security.py -v
```

**Coverage Report:**
```bash
python -m pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

### Test Coverage

The test suite covers:

- ✅ Authentication & Authorization
- ✅ XSS Attack Prevention
- ✅ SQL Injection Prevention
- ✅ CSRF Protection
- ✅ Input Validation
- ✅ Access Control
- ✅ Password Security
- ✅ Lock Mechanism
- ✅ Session Management
- ✅ Security Headers

### Frontend Testing

```bash
cd front-app
npm test
```

---

## 🔒 Security

### Security Measures Implemented

#### 1. Authentication & Authorization
- **JWT Tokens**: Secure, stateless authentication
- **HTTP-Only Cookies**: Prevents XSS-based token theft
- **Token Expiration**: Automatic session timeout
- **Password Hashing**: bcrypt with salt

#### 2. Data Protection
- **Input Validation**: Strict validation on all user inputs
- **Output Encoding**: XSS prevention through HTML escaping
- **Parameterized Queries**: SQL injection prevention
- **HTTPS Ready**: TLS/SSL support for production

#### 3. Security Headers
```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000 (Production)
```

#### 4. Rate Limiting
- API request throttling
- Failed login attempt limits
- DDoS protection mechanisms

### Security Best Practices

#### For Development
1. Never commit `.env` files
2. Use environment variables for sensitive data
3. Regularly update dependencies
4. Run security tests before commits

#### For Production
1. Change all default secrets and keys
2. Enable HTTPS/TLS
3. Configure firewall rules
4. Enable rate limiting
5. Set up monitoring and logging
6. Regular security audits
7. Keep dependencies updated

### Vulnerability Reporting

If you discover a security vulnerability, please open an issue on GitHub with the label "security". 

**Note**: This is an academic project for learning purposes.

---

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/register`
Register a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe"
  }
}
```

#### POST `/api/login`
Authenticate and receive JWT token.

**Request:**
```json
{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe"
  }
}
```

#### POST `/api/logout`
Invalidate current session.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### Notes Endpoints

#### GET `/api/notes`
Retrieve all accessible notes for authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "success": true,
  "notes": [
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Q1 planning meeting...",
      "visibility": "private",
      "is_owner": true,
      "owner_name": "john_doe",
      "created_at": "2026-01-28T10:00:00Z",
      "updated_at": "2026-01-28T15:30:00Z"
    }
  ]
}
```

#### GET `/api/notes/<id>`
Retrieve specific note details.

#### POST `/api/notes`
Create a new note.

**Request:**
```json
{
  "title": "Project Ideas",
  "content": "Innovative solutions for...",
  "visibility": "private"  // Options: private, read, write
}
```

#### PUT `/api/notes/<id>/edit`
Update existing note.

#### POST `/api/notes/<id>/lock`
Acquire edit lock on a note.

#### DELETE `/api/notes/<id>/lock`
Release edit lock on a note.

#### GET `/api/notes/<id>/lock`
Get lock status of a note.

### Error Responses

All endpoints return standard error responses:

**400 Bad Request:**
```json
{
  "success": false,
  "error": "Validation error message"
}
```

**401 Unauthorized:**
```json
{
  "success": false,
  "error": "Authentication required"
}
```

**403 Forbidden:**
```json
{
  "success": false,
  "error": "Access denied"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": "Resource not found"
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## 🚢 Deployment

### Production Deployment Checklist

- [ ] Update all secret keys and passwords
- [ ] Configure environment variables
- [ ] Enable HTTPS/TLS
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Enable rate limiting
- [ ] Set up CDN for static assets
- [ ] Configure CORS for production domains
- [ ] Run security audit
- [ ] Load testing
- [ ] Set up CI/CD pipeline

### Docker Deployment (Optional)

**Dockerfile (Backend):**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY back/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  backend-master:
    build: ./back
    environment:
      - SERVER_MODE=master
      - PORT=5000
    ports:
      - "5000:5000"
  
  backend-replica:
    build: ./back
    environment:
      - SERVER_MODE=replica
      - PORT=5001
    ports:
      - "5001:5001"
  
  frontend:
    build: ./front-app
    ports:
      - "3000:3000"
    depends_on:
      - backend-master
```

### Cloud Platforms

#### AWS Deployment
- **EC2**: Backend application servers
- **RDS**: Production database (PostgreSQL/MySQL)
- **S3**: Static asset hosting
- **CloudFront**: CDN
- **Route 53**: DNS management
- **ELB**: Load balancing

#### Azure Deployment
- **App Service**: Backend hosting
- **Azure SQL Database**: Database
- **Blob Storage**: Static files
- **Azure CDN**: Content delivery
- **Application Gateway**: Load balancing

---

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/macOS
lsof -ti:5000 | xargs kill -9
```

#### Database Locked

**Error:** `database is locked`

**Solution:**
- Ensure no other processes are accessing the database
- Restart the application
- Check file permissions

#### CORS Errors

**Error:** `No 'Access-Control-Allow-Origin' header`

**Solution:**
- Verify CORS configuration in `app.py`
- Check frontend API URL configuration
- Ensure credentials are included in requests

#### JWT Token Expired

**Error:** `Token has expired`

**Solution:**
- Log in again to refresh token
- Adjust `JWT_ACCESS_TOKEN_EXPIRES` in configuration

### Debug Mode

Enable debug logging:

```python
# In app.py
app.config['DEBUG'] = True
app.config['TESTING'] = False

# Set logging level
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. Check the [Documentation](#-documentation)
2. Search [Existing Issues](https://github.com/Vruxak21/Distributed-Secure-Notes-Application/issues)
3. Open a new issue on GitHub
4. Review course materials and resources

---

## 🤝 Contributing

Contributions and suggestions are welcome! This is an academic project developed as part of a Software Architecture and Design course.

### Development Workflow

1. **Fork the Repository**
   ```bash
   git clone https://github.com/Vruxak21/Distributed-Secure-Notes-Application.git
   cd Distributed-Secure-Notes-Application
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add/update tests
   - Update documentation

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   **Commit Message Convention:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test updates
   - `chore:` Build/config changes

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Standards

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Follow standard JavaScript conventions
- **Documentation**: Update README and inline comments
- **Testing**: Maintain test coverage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Vruxak21

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

This project was developed as an academic assignment for the Software Architecture and Design (SAD) course at **Nirma University**.

**Special Thanks:**
- **Course Instructors** - For guidance and support throughout the project
- **Flask Community** - Excellent web framework and documentation
- **React Team** - Powerful UI library
- **OWASP** - Security best practices and guidelines
- **Nirma University** - Academic resources and infrastructure

---

## 📞 About

### Project Information
- **Course**: Software Architecture and Design (SAD)
- **Institution**: Nirma University
- **Semester**: 6
- **Academic Year**: 2024

### Resources
- [GitHub Repository](https://github.com/Vruxak21/Distributed-Secure-Notes-Application)
- [Report Issues](https://github.com/Vruxak21/Distributed-Secure-Notes-Application/issues)

---

<div align="center">

**Developed as an Academic Project**

[⬆ Back to Top](#distributed-secure-notes-application)

</div>




