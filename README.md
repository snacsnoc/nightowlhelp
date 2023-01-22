# Intro
Get a text message at the best time to wake up.

Uses Redis queues to manage SMS jobs

# Environment variables setup
TWILIO_AUTH_TOKEN
TWILIO_ACCOUNT_SID
REDIS_URL

# Run

* Run `python3 -m waitress --listen=*:8080 'app:app'`
* Run `worker2.py`
* Magic