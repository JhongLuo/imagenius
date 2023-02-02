source venv/bin/activate

python3 a1-backend/init_db.py

python3 a1-backend/run_memcache.py &
sleep 3
python3 a1-backend/run.py &
wait