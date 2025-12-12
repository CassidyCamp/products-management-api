export $(grep -v '^#' .env | xargs)

./.venv/Scripts/python -m uvicorn src.main:app --host $HOST --port $PORT --reload
