set -a
source .env
set +a

./.env/Scripts/python uvicorn src.main:app --host $HOST --port $PORT --reload