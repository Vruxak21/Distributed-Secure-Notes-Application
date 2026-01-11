# Project Overview

- Back-end: Python (Flask), SQLite, master/replica architecture

- Front-end: React (Node.js, npm)

- Security: JWT authentication, access control, locking mechanism

# Installation Instructions

## Prerequisites

Before installing and running the project, ensure the following tools are installed on your system:

- **Python 3.10+**  
  Required for the back-end API and services.

- **Node.js & npm**  
  Required to run the **React front-end** (npm is included with Node.js).

- **SQLite3**  
  Used as the database for both master and replica servers.

You can verify the installations with:
```sh
python --version
node --version
npm --version
sqlite3 --version
```




Installation Instructions
=========================
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

Then, run both master and replica scripts as follows:

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

Or you can run the scripts directly:
Windows:
``` batch
./start.bat
```

Linux:
``` sh
./start.sh
```
