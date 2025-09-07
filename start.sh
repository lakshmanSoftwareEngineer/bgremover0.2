#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --max-requests 1000 --max-requests-jitter 50
