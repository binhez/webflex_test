from flask import Flask, jsonify, request, send_file

app = Flask(__name__)


@app.route('/',methods=['GET'])
def hello():
    # Use a breakpoint in the code line below to debug your script.
    name = request.args.get('name')
    if name is None:
        text = 'trả tiền cho anh m'

    else:
        text = name + ': 0337991048'

    return jsonify({"message": text})


# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
