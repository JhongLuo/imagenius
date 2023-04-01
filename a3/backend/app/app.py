from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask on AWS Lambda using Zappa!"

if __name__ == '__main__':
    app.run()
