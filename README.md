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
