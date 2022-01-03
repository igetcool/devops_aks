import platform
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "I'm in {}".format(platform.node())

if __name__ == '__main__':
    print('aa')
    app.run(host='127.0.0.1', port=8080)
