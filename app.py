from flask import (
    Flask, jsonify, request
)

app = Flask(__name__)


@app.route('/tasks', methods=['POST'])
def assign_tasks():
    #if (
    #    request.method != 'POST' or
    #    request.headers['content-type'] != 'application/json'
    #):
    #    return jsonify(['NOK']), 405

    tasks = request.data
    return tasks


if __name__ == '__main__':
    app.run(debug=True)
