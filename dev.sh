export ENVIRONMENT=local

uvicorn app:app --host 0.0.0.0 --port 5005 --reload
