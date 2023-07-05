# Crossover Grid Server

## File Structure
```
Crossover-Grid-Server/
│
├─ server/  # server scripts
│   └─ Server.py
|
└─ app.py  # server url endpoints
```

## How to run the server

1. Clone the repo `git clone https://github.com/maxsauers13/crossover-grid-server.git && cd Crossover-Grid-Server`.
2. Install dependencies `pip install -r requirements.txt`.
3. Open up a terminal and launch `gunicorn --workers <Number of Workers> --bind <IP Address>:<Port Number> 'app:app'`.