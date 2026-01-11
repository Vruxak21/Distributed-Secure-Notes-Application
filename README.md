# Distributed Secure Application
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Node](https://img.shields.io/badge/Node.js-LTS-green?logo=node.js)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-lightgrey)



## Project Overview

This project implements a secure, distributed architecture ensuring data consistency and access control.

### Architecture


* **Back-end:** Python (Flask), SQLite.
    * **Architecture:** Master/Replica synchronization.
* **Front-end:** React (Node.js ecosystem).
* **Security:** * JWT (JSON Web Token) Authentication.
    * Role-based Access Control.
    * Concurrency Locking Mechanism.

## Prerequisites

Ensure the following tools are installed on your system before proceeding:

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.10+` | Backend API and services. |
| **Node.js** | `LTS` | React frontend runtime (includes npm). |
| **SQLite3** | `Latest` | Database engine for Master/Replica. |

**Verify installations:**
```bash
python --version
node --version
npm --version
sqlite3 --version
```


# Installation Instructions
### Back
```
cd back
python -m venv .venv
```
Windows:
``` batch
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux:
``` sh
source .venv/bin/activate
pip install -r requirements.txt
```

### Front
```sh
cd front
npm i
```


# Tests

To run the backend automated tests, follow one of the options below.

### Windows (script)

If you are using Windows, you can run the tests using the provided script:
```sh
./back/run_tests.bat
```
### Manual execution

You can also run the tests manually:
```
cd back
source .venv/bin/activate
pip install -r test_requirements.txt
python -m pytest tests/test_security.py -v
```

# Launch

Option A: Quick Start (Recommended)
Use the global launch scripts to start the Backend (Master & Replica) and Frontend simultaneously.

Or you can run the scripts directly:
Windows:
``` batch
./start.bat
```

Linux:
``` sh
./start.sh
```

Option B: Manual Launch
If you prefer to run services manually in separate terminals:

1. Start Backend (Master & Replica)
Windows:
``` batch
.\scripts\windows\run_master.bat
.\scripts\windows\run_replica.bat
```
Linux:
``` sh
./scripts/linux/run_master.sh &
./scripts/linux/run_replica.sh &
```
2. Start Frontend
```sh
cd front
npm start
```




