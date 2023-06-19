from flask import Flask, request

app = Flask(__name__)


# post form data: {"string": "This is uploaded sample", "int": 1234567890}

@app.route('/hello', methods=['POST'])
def hello():
    print(request.json)
    return {
        "state": 0,
        "err": None,
        "data": ["this is a test ret data"],
    }


if __name__ == "__main__":
    app.run()
    # run and visit localhost:5000/hello/
