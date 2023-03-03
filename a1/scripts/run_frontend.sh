cd ./a1-frontend

pid_5173=$(lsof -ti tcp:5173)

kill -9 $pid_5173

npm install
npm start