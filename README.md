Installation Instructions
=========================
```
cd back
.venv\Scripts\activate
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
