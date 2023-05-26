from flask import Flask

app = Flask(__name__)


@app.route('/hello/<uname>', methods=['GET'])
def hello(uname):
    ret = {
        "msg": "Hello," + uname
    }
    return {
        "state": 0,
        "err": None,
        "data": ret
    }


if __name__ == "__main__":
    app.run()
    # run and visit localhost:5000/hello/