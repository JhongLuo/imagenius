cd ./a1-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../

pid_5000=$(lsof -ti tcp:5000)
pid_5001=$(lsof -ti tcp:5001)

kill -9 $pid_5000
kill -9 $pid_5001

source a1-backend/venv/bin/activate

python3 a1-backend/init_db.py

python3 a1-backend/run_memcache.py &
sleep 3
python3 a1-backend/run.py &
#wait